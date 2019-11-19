from django.db import models
from .orders import Order
from .products import Product

class OrderProduct(models.Model):
    """
    Creates the join table for the relationship between orders and products
    """

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='cart')