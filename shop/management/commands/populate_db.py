# shop/management/commands/populate_db.py
# Create directories: shop/management/commands/

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Home & Kitchen', 'description': 'Home appliances and kitchenware'},
            {'name': 'Sports', 'description': 'Sports equipment and gear'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(**cat_data)
            categories.append(category)
            if created:
                self.stdout.write(f'  Created category: {category.name}')
        
        self.stdout.write('Creating products...')
        
        # Electronics
        electronics_products = [
            {'name': 'Wireless Headphones', 'price': 2999, 'description': 'Premium noise-cancelling wireless headphones with 30-hour battery life'},
            {'name': 'Smart Watch', 'price': 4999, 'description': 'Fitness tracker with heart rate monitor and GPS'},
            {'name': 'Laptop Stand', 'price': 1499, 'description': 'Ergonomic aluminum laptop stand'},
            {'name': 'USB-C Hub', 'price': 1999, 'description': '7-in-1 USB-C hub with HDMI and card reader'},
            {'name': 'Bluetooth Speaker', 'price': 3499, 'description': 'Portable waterproof speaker with bass boost'},
        ]
        
        # Clothing
        clothing_products = [
            {'name': 'Cotton T-Shirt', 'price': 499, 'description': 'Comfortable 100% cotton t-shirt in various colors'},
            {'name': 'Denim Jeans', 'price': 1999, 'description': 'Classic fit denim jeans'},
            {'name': 'Running Shoes', 'price': 2999, 'description': 'Lightweight running shoes with cushioned sole'},
            {'name': 'Hoodie', 'price': 1499, 'description': 'Warm fleece hoodie with kangaroo pocket'},
            {'name': 'Backpack', 'price': 1799, 'description': 'Durable backpack with laptop compartment'},
        ]
        
        # Books
        books_products = [
            {'name': 'Python Programming', 'price': 599, 'description': 'Complete guide to Python programming'},
            {'name': 'Data Science Handbook', 'price': 899, 'description': 'Comprehensive data science and ML book'},
            {'name': 'Fiction Novel', 'price': 399, 'description': 'Bestselling fiction novel'},
            {'name': 'Self-Help Book', 'price': 449, 'description': 'Guide to personal development'},
        ]
        
        # Home & Kitchen
        home_products = [
            {'name': 'Coffee Maker', 'price': 3999, 'description': 'Programmable coffee maker with timer'},
            {'name': 'Blender', 'price': 2499, 'description': 'High-power blender for smoothies'},
            {'name': 'Cookware Set', 'price': 4999, 'description': 'Non-stick cookware set of 5 pieces'},
            {'name': 'Water Bottle', 'price': 499, 'description': 'Insulated stainless steel water bottle'},
        ]
        
        # Sports
        sports_products = [
            {'name': 'Yoga Mat', 'price': 799, 'description': 'Non-slip yoga mat with carrying strap'},
            {'name': 'Dumbbell Set', 'price': 2999, 'description': 'Adjustable dumbbell set 5-25kg'},
            {'name': 'Resistance Bands', 'price': 699, 'description': 'Set of 5 resistance bands'},
            {'name': 'Jump Rope', 'price': 299, 'description': 'Speed jump rope for cardio'},
        ]
        
        all_products = [
            (categories[0], electronics_products),
            (categories[1], clothing_products),
            (categories[2], books_products),
            (categories[3], home_products),
            (categories[4], sports_products),
        ]
        
        for category, products in all_products:
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'category': category,
                        'stock': random.randint(10, 100),
                        'popularity_score': round(random.uniform(0.3, 0.9), 2),
                        'rating': round(random.uniform(3.5, 5.0), 1),
                    }
                )
                if created:
                    self.stdout.write(f'  Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))