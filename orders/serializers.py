from django.db.models import F, Sum
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ValidationError, NotFound
from orders.models import Order, CartItem, Product
from orders.mixins import validateCartItemMixin
from orders.constants import (
    SUPPORTED_MARKETPLACES,
    SUPPORTED_CURRENCIES
)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("id_lengow", "title", "price_unit", "category")


class CartItemSerializer(ModelSerializer):
    """Represents a line in the Cart of an Order."""

    product = ProductSerializer()
    price = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "price")

    def get_price(self, obj):
        return obj.quantity * obj.product.price_unit



class CartItemCreateSerializer(validateCartItemMixin, ModelSerializer):
    """Add one or more Product to the Cart of an Order."""

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


    def validate(self, attrs):

        try:
            order_id = self.context["view"].kwargs.get("order_pk")
            attrs["order"] = Order.objects.get(id=int(order_id))
        except:
            raise NotFound(f"Order with id `{order_id}` could not be found.")

        product = attrs["product"]
        if CartItem.objects.filter(order_id=order_id, product=product).exists():
            raise ValidationError(
                f"The Product `{product.id}` already exist on the order `{order_id}`."
            )

        return attrs


class CartItemUpdateSerializer(validateCartItemMixin, ModelSerializer):
    """Change the quantity of a CartItem."""

    class Meta:
        model = CartItem
        fields = ("quantity",)



class OrderSerializer(ModelSerializer):
    """Serialize an Order with its Cart and Product(s)."""
    amount = SerializerMethodField()
    cart = CartItemSerializer(source="cart_items", many=True)

    class Meta:
        model = Order
        fields = ('id', 'marketplace', 'amount', 'currency', "cart")

    def get_amount(self, obj):
        # Compute Order amount based on related entities
        total_cart = (
            CartItem.objects
            .filter(order=obj)
            .aggregate(total=Sum(F('quantity') * F('product__price_unit')))['total']
        )
        return total_cart + obj.shipping_amount


class OrderCreateSerializer(ModelSerializer):
    """Create a basic Order."""

    class Meta:
        model = Order
        fields = ('marketplace', 'currency')
    
    def validate_marketplace(self, value):
        if value not in SUPPORTED_MARKETPLACES:
            raise ValidationError(f"Marketplace {value} is not supported.")
        return value
    
    def validate_currency(self, value):
        if value not in SUPPORTED_CURRENCIES:
            raise ValidationError(f"Currency {value} is not supported.")
        return value
