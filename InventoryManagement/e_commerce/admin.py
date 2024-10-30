from django.contrib import admin
from .models import Cart, CartItem, OrderRequisition, OrderRequisitionItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderRequisition)
admin.site.register(OrderRequisitionItem)
# Register your models here.
