from .models import Product_catagory,Product,Order,Order_detail,Topping

prod = Product.objects.all()

print(prod)
