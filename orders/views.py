from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product_catagory,Product,Order,Order_detail,Topping
from .sendEmail import send_HTML_Email
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated :
        print('authenticated')
    else:
        print('not authenticated')
    
    products = list(Product.objects.all().order_by('catagory__name'))
    catagorys = list(Product_catagory.objects.all())
    toppings = list(Topping.objects.all().order_by('name'))
    subsextra = list(Product.objects.filter(catagory__name = "SubsExtra"))
    context = {
        'Products' : products,
        'Catagorys': catagorys,
        'Toppings' : toppings,
        'SubsExtra' : subsextra
    }
    print('query done')
    return render(request, 'orders/index.html',context)

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None :
            login(request, user)
            print('authenticated',username)
            messages.success(request, "Logged in Successfully")
            return redirect('orders_index')
        messages.error(request, " Invalid credentials")
        print('not authenticated')
        return redirect('orders_index')
    else:
        return HttpResponseRedirect(reverse('orders_index'))

def blog(request):
    return render(request, 'orders/blog.html')

def menu(request):
    products = list(Product.objects.all().order_by('catagory__name'))
    catagorys = list(Product_catagory.objects.all())
    toppings = list(Topping.objects.all().order_by('name'))
    subsextra = list(Product.objects.filter(catagory__name = "SubsExtra"))
    context = {
        'Products' : products,
        'Catagorys': catagorys,
        'Toppings' : toppings,
        'SubsExtra' : subsextra
    }
    return render(request, 'orders/menu.html',context)

def checkout(request):
    # only if request method is post prevent url bar hit enter again n again
    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        cartItems = json.loads(request.POST['cartitems'])

        # assign required variable to 0
        total_amount = 0
        extcost = 0

        # get user instance 
        user = User.objects.get(username=username)
        
        # create & save Order instance
        order = Order(status="P",amount=0,user=user)
        order.save()
        
        # loop for items in the shopping cart with not none
        for item in cartItems:
            if item is not None :
                for extras in item['extras']:
                    extkey = list(extras.keys())
                    extcost += float(extras[extkey[0]])
                prodid = item['prodid']
                size = item['size'][0].upper()
                quantity = item['quantity']
                topping_list = item['topping']
                product = Product.objects.get(pk=prodid)

                # do not rely on client side rate get rates from server / model
                rate = product.price_small if size=="S" else product.price_large

                # calculate total amount with extras cost
                total_amount += (float(rate) + extcost) * quantity

                # create order_detail instance
                order_detail = Order_detail(order_detail=order,product_detail=product,size=size,quantity=quantity,rate=rate)
                order_detail.save()

                # add toppings to order_detail instance
                for topping in topping_list:
                    topping_to_add = Topping.objects.get(name=topping)
                    order_detail.topping.add(topping_to_add)
                
                item['rate'] = float(rate)
                item['extcost'] = float(extcost)
                print('prodid',prodid,'product',product,'size',size,'rate',rate,'qty',quantity,'topping',topping_list)

        # update total_amount to Order instance
        order.amount = round(total_amount,2)

        # context for email to client
        # print(cartItems)
        context = {
            'first_name' : first_name,
            'cartItems' : cartItems
        }
        # print('order',order)
        # print('order_detail_Order ID:',order_detail.order_detail)
        # print('order_detail',order_detail)
        #result = send_HTML_Email([email],"Pinochio's Order Placed","orders/checkoutMail.html",context)

        messages.success(request, f'Thanks {first_name} your order is placed and confirmation mail sent.')
    return HttpResponseRedirect(reverse('orders_index'))

def services(request):
    return render(request, 'orders/services.html')

def about(request):
    return render(request, 'orders/about.html')

def contact(request):
    return render(request, 'orders/contact.html')

def contactSubmitted(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        mail_to = [request.POST['email']]
        msg = request.POST['msg']
        messages.success(request, f'Thanks {fullname} for contacting Harish Ahuja')
        if request.POST['subject']:
            subject = request.POST['subject']
        else :
            subject = "Welcome to Pinochio's pizza & subs"
        context = {
            'fullname' : fullname,
            'msg' : msg
        }
        result = send_HTML_Email(to=mail_to,subject=subject,template_name='orders/contactSubmitted.html',context=context)
        print(result)
    return HttpResponseRedirect(reverse('orders_index'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('orders_index'))

def signup(request):
    if request.POST :
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username,email=email)
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            messages.success(request, f'Welcome {first_name}')
            subject = "Welcome to Pinochio's Pizza & Subs"
            context = {
                'user' : user,
                'password' : password
            }
            result = send_HTML_Email(to=[email],subject=subject,template_name='orders/signupMail.html',context=context)
            print(result)
        except :
            messages.error(request, f'Login Faield Username {username} already taken')

    return HttpResponseRedirect(reverse('orders_index'))
