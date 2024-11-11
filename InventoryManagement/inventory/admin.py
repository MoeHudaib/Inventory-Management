from django.contrib import admin
from .models import Stock, Inventory, InventoryLocation, Category, Color

class ProductColorsAdmin(admin.ModelAdmin):
    list_display = ['rgb']
    search_fields = ('name', 'rgb')
admin.site.register(Color, ProductColorsAdmin)
admin.site.register(InventoryLocation)
admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(Stock)
# Register your models here.
