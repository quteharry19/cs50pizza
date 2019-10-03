from django.contrib import admin
from .models import Product_catagory, Product, Order, Order_detail, Topping

# Register your models here.
class Product_admin(admin.ModelAdmin):
    list_display = ("catagory","name", "generic_name" ,"price_small","price_large")
    search_fields = ["catagory__name","name","generic_name"]
    list_filter = ["catagory__name","generic_name"]
    list_editable = ["generic_name","price_small","price_large"]

class Order_admin(admin.ModelAdmin):
    list_display = ("user","status","amount")

class Order_detail_admin(admin.ModelAdmin):
    list_display = ("order_detail","product_detail","quantity","size")
    filter_horizontal = ("topping",)

admin.site.register(Product_catagory)
admin.site.register(Product, Product_admin)
admin.site.register(Order, Order_admin)
admin.site.register(Order_detail, Order_detail_admin)
admin.site.register(Topping)