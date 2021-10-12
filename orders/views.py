from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from orders.models import Order, CartItem, Product
from orders.serializers import (
    CartItemCreateSerializer,
    OrderSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    ProductSerializer
)

class OrderViewset(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    """
    List all existing orders or retrieve a specific one.
    Filter by marketplace, currency, category or both using query parameters.
    Create a new order using supported marketplace and currencies.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_params = self.request.query_params
        if "marketplace" in self.request.query_params:
            queryset = queryset.filter(marketplace=query_params["marketplace"])
        if "currency" in self.request.query_params:
            queryset = queryset.filter(currency=query_params["currency"])
        if "category" in self.request.query_params:
            queryset = (
                queryset.filter(
                    cart_items__product__category__contains=query_params["category"]
                )
            )
        return queryset


class CartItemViewset(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    """
    This viewset is nested within the order api, 
    so cart items will always be filtered based on its related Order.
    Show all the lines of the Cart of an Order.
    Create a new line with a Product and a quantity.
    Update quantity of a line.
    Remove a line from the cart of an Order.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(order_id=self.kwargs.get("order_pk"))
    
    def get_serializer_class(self):
        if self.action == "create":
            return CartItemCreateSerializer
        elif self.action == "partial_update":
            return CartItemUpdateSerializer
        return super().get_serializer_class()
    

class ProductViewset(ListModelMixin, GenericViewSet):
    """List all products available for purchase."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer