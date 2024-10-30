from . import views
from django.urls import path

app_name = "sales"

urlpatterns = [
    path('sales-list/', views.sales_list, name='sales-list'),
    path('receipt', views.receipt, name='receipt'),
    path('delete-sale', views.delete_sale, name='delete-sale'),
    
]