from django.db import models
from django.db.models.fields import FloatField

class Order(models.Model):

    identifier = models.CharField(max_length=20, null=True, default=None)
    mrid = models.CharField(max_length=20, null=True, default=None)
    refid = models.CharField(max_length=20, null=True, default=None)
    marketplace = models.CharField(max_length=100)
    purchased_at = models.DateTimeField(null=True, default=None)
    
    amount = models.FloatField()
    shipping_amount = models.FloatField(default=0)
    commission_amount = models.FloatField(default=0)
    processing_fee = models.FloatField(default=0)
    currency = models.CharField(max_length=3)

class Product(models.Model):

    id_lengow = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    price_unit = models.FloatField()
    category = models.CharField(max_length=200) # This one should have its dedicated Model

class CartItem(models.Model):

    order = models.ForeignKey(Order, related_name="cart_items", on_delete=models.deletion.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.deletion.CASCADE)
    quantity = models.IntegerField(default=1)

