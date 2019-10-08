from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="orders_index"),
    path("login", views.login_view, name="login_view"),
    path("blog", views.blog, name="blog"),
    path("menu", views.menu, name="menu"),
    path("services", views.services, name="services"),
    path("about", views.about, name="about"),
    path("locate", views.locate, name="locate"),
    path("contact", views.contact, name="contact"),
    path("contactSubmitted", views.contactSubmitted, name="contactSubmitted"),
    path("logout", views.logout_view, name="logout_view"),
    path("signup", views.signup, name="signup"),
    path("checkout", views.checkout, name="checkout"),
    path("checkorderid/<int:order_id>",views.checkorderid, name="checkorderid"),
    path("checkorder/<str:username>", views.checkorder, name="checkorder"),
    path("updateOrderStatus/<int:order_id>", views.updateOrderStatus, name="updateOrderStatus")
]
