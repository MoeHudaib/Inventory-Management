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
    address=models.TextField(null=True,blank=True)
    city= models.CharField(max_length=100,null=True,blank=True)
    postcode= models.IntegerField(null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    email= models.CharField(max_length=100,null=True,blank=True)
    additional_info=models.TextField(null=True,blank=True)
    amount=models.CharField(max_length=100,null=True,blank=True)
    date= models.DateField(default=date.today,null=True,blank=True)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default= False ,null= True)
    done = models.BooleanField(default=False)

    def __str__(self):
      return self.user.username
    
class OrderItem(models.Model):    
    order= models.ForeignKey(Order,on_delete=models.CASCADE,null=True) 
    product= models.ForeignKey("inventory.Stock", models.CASCADE, null=True, blank= True)
    image= models.ImageField(upload_to="product_images/Order_Img", editable=False)
    quantity= models.CharField(max_length=100)
    price= models.CharField(max_length=100, editable=False)
    total= models.CharField(max_length=1000, editable=False)

    def __str__(self):
        return self.order.user.username
    
    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.unit_cost
            self.image.url = self.product.image.url
        self.total = str(float(self.price)*float(self.quantity))
        super().save(*args, **kwargs)
