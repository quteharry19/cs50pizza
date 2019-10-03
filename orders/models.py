from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# models.

class Product_catagory(models.Model):
    name = models.CharField("Catagory Name",max_length=64)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    catagory = models.ForeignKey(
                Product_catagory, on_delete=models.CASCADE, related_name="product_catagory")
    name = models.CharField(max_length=64)
    generic_name = models.CharField(max_length=30,blank=True)
    image = models.ImageField(
                verbose_name="Product Image", upload_to="images/", default=None, blank=True)
    price_small = models.DecimalField("Prize for Small", max_digits=5, decimal_places=2)
    price_large = models.DecimalField("Prize for Large", max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} -{self.catagory} - {self.generic_name}"

class Topping(models.Model):
    name = models.CharField("Topping",max_length=25)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    STATUS = [
        ("P","Pending"),
        ("C","Complete"),
        ("D","Delivered")
    ]
    status = models.CharField(max_length=1,choices=STATUS,default="P")
    amount = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_orders")
    #date = models.DateTimeField()

    def __str__(self):
        return f"id: {self.id} {self.user} {self.status} {self.amount}"

class Order_detail(models.Model):
    SIZES = [
        ('S','Small'),
        ('L','Large')
    ]
    order_detail = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_details")
    product_detail = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_detail",default=0)
    size = models.CharField(max_length=1,choices=SIZES,default="S")
    quantity = models.IntegerField()
    rate = models.FloatField(default=0)
    topping = models.ManyToManyField(Topping,related_name="order_topping",blank=True)

    def topping_list(self):
        top_list = [top.name for top in self.topping.all() ]
        return top_list
        
    def __str__(self):
        return f"id: {self.id} - {self.quantity} - {self.topping.in_bulk()}"

# class OrderManager(models.Manager):
#     def topping_check(self,topping_allowed,topping_selected):

#         if topping_allowed != topping_selected:
#             return False
#         else:
#             return True
