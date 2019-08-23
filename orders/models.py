from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product_catagory(models.Model):
    Catagory_name = models.CharField("Catagory Name",max_length=64)

    def __str__(self):
        return f"{self.Catagory_name}"

class Product(models.Model):
    catagory = models.ForeignKey(Product_catagory,on_delete=models.CASCADE,related_name="product_catagory")
    product_name = models.CharField(max_length=64)
    prize_small = models.FloatField("Prize for Small")
    prize_large = models.FloatField("Prize for Large")

    def __str__(self):
        return f"{self.catagory} {self.product_name} {self.prize_small} {self.prize_large}"

class Topping(models.Model):
    topping_name = models.CharField("Topping",max_length=25)

    def __str__(self):
        return f"{self.topping_name}"

class Order(models.Model):
    STATUS = [
        ("P","Pending"),
        ("C","Complete"),
        ("D","Delivered")
    ]
    status = models.CharField(max_length=1,choices=STATUS,default="P")
    amount = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_orders")

    def __str__(self):
        return f"{self.user} {self.status} {self.amount}"

class Order_detail(models.Model):
    order_detail = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_details")
    product_detail = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_detail",default=0)
    quantity = models.IntegerField()
    rate = models.FloatField(default=0)
    topping = models.ManyToManyField(Topping,related_name="order_topping",blank=True)

    def __str__(self):
        return f"{self.order_detail} {self.product_detail} {self.topping} {self.rate} {self.quantity}"











