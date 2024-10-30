from django.contrib import admin
from .models import Stock, Inventory, InventoryLocation, Category, ProductColors

@admin.register(ProductColors)
class ProductColorsAdmin(admin.ModelAdmin):
    list_display = ('product', 'rgb')
    search_fields = ('product__name', 'rgb')
admin.site.register(InventoryLocation)
admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(Stock)
# Register your models here.
