# shop/admin.py
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserInteraction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'popularity_score', 'rating']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'popularity_score', 'rating']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'get_total']
    
    def get_total(self, obj):
        return f"₹{obj.get_total()}"
    get_total.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_subtotal']
    
    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_amount', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'interaction_type', 'timestamp']
    list_filter = ['interaction_type', 'timestamp']
    search_fields = ['user__username', 'product__name']