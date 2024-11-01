from django.db import models
from django.utils import timezone

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    rows_number = models.IntegerField()
    columns_number = models.IntegerField()
    layers_number = models.IntegerField()

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return self.name

class InventoryLocation(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    row = models.IntegerField(null=True)
    column = models.IntegerField(null=True)
    layer = models.IntegerField(null=True)
    quantity = models.FloatField(default=0, blank=True, null=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, null=True, blank=True)
    reserved = models.BooleanField(default=True, null=True)

    class Meta:
        unique_together = ('inventory', 'row', 'column', 'layer')

    def __str__(self):
        return f"Row {self.row}, Column {self.column}, Layer {self.layer}"

class Category(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True) 
    date_added = models.DateTimeField(default=timezone.now, null=True, blank=True) 
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Stock(models.Model):
    UNIT_TYPES = [
        ('kg', 'Kilogram'),
        ('l', 'Liter'),
        ('m', 'Meter'),
    ]

    vocab_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, null=True)
    description1 = models.TextField(null=True)
    description2 = models.TextField(null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='stock_images/', null=True, blank=True)
    unit = models.CharField(max_length=255, choices=UNIT_TYPES, null=True)
    unit_cost = models.FloatField(null=True, blank=True)
    stocks_on_hand = models.IntegerField(default=0)
    stocks_committed = models.IntegerField(default=0)
    stocks_availability = models.IntegerField(editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    stored_stocks = models.IntegerField(default=0)
    exp_date = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    sold_number = models.IntegerField(default=0)
    threshold = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    def is_low_stock(self):
        return self.stocks_availability < self.threshold

    def save(self, *args, **kwargs):
        if self.pk:
            from pos.models import InboundItem  # Avoid circular import
            material_inbounds = InboundItem.objects.filter(material=self)
            self.stocks_on_hand = sum(material.quantity for material in material_inbounds)
            from e_commerce.models import OrderRequisitionItem  # Avoid circular import
            material_orders_committed = OrderRequisitionItem.objects.filter(
                material=self,
                order_requisition__done=False
            )
            self.stocks_committed = sum(material.quantity for material in material_orders_committed)
            from pos.models import OutboundItem
            material_sold_number = OutboundItem.objects.filter(
                material=self,
            )
            self.sold_number = sum(material.quantity for material in material_sold_number)

        self.stocks_availability = self.stocks_on_hand - self.stocks_committed
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

import re
from django.core.exceptions import ValidationError

class ProductColors(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='colors')
    rgb = models.CharField(max_length=7)

    class Meta:
        verbose_name = 'Product Color'
        verbose_name_plural = 'Product Colors'
        unique_together = ('product', 'rgb')

    def clean(self):
        super().clean()
        if not re.match(r'^#[0-9A-Fa-f]{6}$', self.rgb):
            raise ValidationError('RGB must be in the format #RRGGBB.')

    def __str__(self):
        return f"{self.product.name} - {self.rgb}"
