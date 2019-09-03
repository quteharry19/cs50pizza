from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product_catagory,Product,Order,Order_detail,Topping
from .sendEmail import send_HTML_Email

# Create your views here.
def index(request):
    if request.user.is_authenticated :
        print('authenticated')
    else:
        print('not authenticated')
    
    context = {
        'Products' : Product.objects.all(),
        'Catagorys': Product_catagory.objects.all()
    }
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
    return render(request, 'orders/menu.html')

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
