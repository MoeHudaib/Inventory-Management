from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.apps import apps 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    total_items = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_price = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user} - Status: {'Active' if self.active else 'Inactive'}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-date_created']

class CartItem(models.Model):
    item = models.ForeignKey('inventory.Stock', on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Cart ID {self.cart.id if self.cart else 'N/A'}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('item', 'cart')

class OrderRequisition(models.Model):
    SHIPPING_TYPES = [
        ('ground', 'Ground'),
    ]
    PAYMENT_TYPES = [
        ('cash', 'Cash'),
        ('credit card', 'Credit Card'),
    ]
    cart = models.ForeignKey(Cart, models.CASCADE, null=True, blank=True)
    inventory = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, related_name='order_requisitions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_requisitions')
    date_created = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateField()
    shipped_via = models.CharField(max_length=50, choices=SHIPPING_TYPES, null=True, blank=True)
    payment_terms = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    total_price = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=0)
    done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            MaterialOrderRequisition = apps.get_model('sales', 'MaterialOrderRequisition')
            material_orders = MaterialOrderRequisition.objects.filter(order_requisition=self)
            self.total_price = sum(
                abs(material.quantity) * material.material.unit_cost
                for material in material_orders
                if material.material.unit_cost is not None
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order Requisition ID: {self.id} - Done: {self.done}'

class OrderRequisitionItem(models.Model):
    order_requisition = models.ForeignKey(OrderRequisition, on_delete=models.CASCADE, related_name='material_orders', null=True, blank=True)
    material = models.ForeignKey('inventory.Stock', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    sold_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    number_sold = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.order_requisition.done and self.active:
            self.sold_date = timezone.now()
            self.active = False
        super().save(*args, **kwargs)
