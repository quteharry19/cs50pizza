from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
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
    
    context = get_menu_context()

    return render(request, 'orders/index.html',context)

def get_menu_context():
    products = list(Product.objects.all().values().order_by('catagory__name'))
    catagorys = list(Product_catagory.objects.all().prefetch_related('product_catagory'))
    toppings = list(Topping.objects.all().values('name').order_by('name'))
    subsextra = list(Product.objects.filter(catagory__name = "SubsExtra").values())
    toppings = [top['name'] for top in toppings ]
    context = {
        'Products' : products,
        'Catagorys': catagorys,
        'Toppings' : toppings,
        'SubsExtra' : subsextra
    }
    print('queryset complete')

    return context

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
    context = get_menu_context()

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
                extkeys = []
                extcost = 0
                for extras in item['extras']:
                    extkey = list(extras.keys())
                    extcost += float(extras[extkey[0]])
                    extkeys.append(extkey)
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
                item['extkeys'] = extkeys
                item['itemcost'] = float((item['rate'] + item['extcost']) * item['quantity'])

                for ext in extkeys:
                    extprod = Product.objects.filter(name=ext[0]).first()
                    rate = extprod.price_small
                    order_detail = Order_detail(order_detail=order,product_detail=extprod,size="S",quantity=1,rate=rate)
                    order_detail.save()


        # update total_amount to Order instance
        order.amount = round(total_amount,2)
        order.save()
        # context for email to client
        context = {
            'first_name' : first_name,
            'order_id' : order.id,
            'order_status' : order.status,
            'cartItems' : cartItems,
            'absolute_uri' : request.build_absolute_uri(f'/checkorderid/{order.id}'),
            'total_amount' : round(total_amount,2)
        }
        result = send_HTML_Email([email],"Pinochio's Order Placed","orders/checkoutMail.html",context)

        messages.success(request, f'Thanks {first_name} your order is placed and confirmation mail sent.')
    return HttpResponseRedirect(reverse('orders_index'))

def checkorderid(request,order_id):
    try:
        order_detail = Order_detail.objects.filter(order_detail__id=order_id).prefetch_related('topping')
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404("Order Does Not Exists")
    
    status_list = [ list1[1] for list1 in order.STATUS ] 
    context = {
        'order_id' : order_id,
        'order_status' : order.get_status_display(),
        'order_amount' : float(order.amount),
        'status_options' : status_list,
        'OrderItems' : order_detail
    }
    return render(request, 'orders/checkorder.html',context)

def checkorder(request,username):
    user = User.objects.get(username=username)
    if user.is_superuser:
        orders = Order.objects.all().order_by('-status','-id')
    else:
        orders = Order.objects.filter(user=user).order_by('-status','-id')
    context = {
        'user' : user,
        'orders' : orders
    }
    return render(request, 'orders/yourorders.html',context)

def updateOrderStatus(request,order_id):
    order = Order.objects.get(pk=order_id)
    order_status = request.POST['order_status']
    order.status = order_status[0]
    order.save()
    return HttpResponseRedirect(reverse('checkorderid', args=(order_id,)))

def services(request):
    return render(request, 'orders/services.html')

def about(request):
    return render(request, 'orders/about.html')

def locate(request):
    return render(request, 'orders/locate.html')

def contact(request):
    return render(request, 'orders/contact.html')

def contactSubmitted(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        mail_to = [request.POST['email']]
        msg = request.POST['msg']
        messages.success(request, f'Thanks {fullname} for contacting Harish Ahuja')

        try:
            subject = request.POST['subject']
        except :
            subject = "Welcome to Pinochio's pizza & subs"
            
        context = {
            'fullname' : fullname,
            'subject' : subject,
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
