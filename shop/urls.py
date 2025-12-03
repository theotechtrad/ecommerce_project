# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('product-feedback/<int:pk>/', views.product_feedback, name='product_feedback'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]