from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.apps import apps 
from datetime import date

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)    
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    contry= models.CharField(max_length=100)
    address=models.TextField()
    city= models.CharField(max_length=100)
    state= models.CharField(max_length=100)
    postcode= models.IntegerField()
    phone=models.IntegerField()
    email= models.CharField(max_length=100)
    additional_info=models.TextField()
    amount=models.CharField(max_length=100)
    date= models.DateField(default=date.today)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default= False ,null= True)
    done = models.BooleanField(default=False)

    def __str__(self):
      return self.user.username
    
class OrderItem(models.Model):    
    order= models.ForeignKey(Order,on_delete=models.CASCADE,null=True) 
    product= models.ForeignKey("inventory.Stock", models.CASCADE, null=True, blank= True)
    image= models.ImageField(upload_to="product_images/Order_Img")
    quantity= models.CharField(max_length=100)
    price= models.CharField(max_length=100)
    total= models.CharField(max_length=1000)
    def __str__(self):
      return self.order.user.username