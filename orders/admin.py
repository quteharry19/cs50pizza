from django.contrib import admin
from .models import Product_catagory, Product, Order, Order_detail, Topping

# Register your models here.
class Product_admin(admin.ModelAdmin):
    list_display = ("catagory","product_name","prize_small","prize_large")
    search_fields = ["catagory__Catagory_name","product_name"]

class Order_admin(admin.ModelAdmin):
    list_display = ("user","status","amount")

class Order_detail_admin(admin.ModelAdmin):
    list_display = ("order_detail","product_detail","quantity")
    filter_horizontal = ("topping",)

admin.site.register(Product_catagory)
admin.site.register(Product, Product_admin)
admin.site.register(Order, Order_admin)
admin.site.register(Order_detail, Order_detail_admin)
admin.site.register(Topping)