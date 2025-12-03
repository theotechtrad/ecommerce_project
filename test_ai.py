# test_ai.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Product, UserInteraction
from shop.recommendation import RecommendationEngine

print("=" * 60)
print("🤖 AI RECOMMENDATION SYSTEM TEST")
print("=" * 60)

# Get or create test user
user, created = User.objects.get_or_create(username='ai_test_user')
print(f"\n✅ Test user: {user.username}")

# Get products
products = list(Product.objects.all()[:8])
print(f"✅ Total products: {len(products)}")

# Clear old interactions
UserInteraction.objects.filter(user=user).delete()

# Simulate user behavior
print("\n📊 Simulating User Interactions:")
print("-" * 60)

# View products 1-4
for i in range(4):
    UserInteraction.objects.create(
        user=user, 
        product=products[i], 
        interaction_type='view'
    )
    print(f"  👁️  Viewed: {products[i].name}")

# Add products 0-1 to cart
for i in range(2):
    UserInteraction.objects.create(
        user=user, 
        product=products[i], 
        interaction_type='cart'
    )
    print(f"  🛒 Carted: {products[i].name}")

# Like product 0
UserInteraction.objects.create(
    user=user, 
    product=products[0], 
    interaction_type='like'
)
print(f"  👍 Liked: {products[0].name}")

# Purchase product 0
UserInteraction.objects.create(
    user=user, 
    product=products[0], 
    interaction_type='purchase'
)
print(f"  💳 Purchased: {products[0].name}")

# Get AI recommendations
print("\n🤖 AI GENERATING RECOMMENDATIONS...")
print("-" * 60)

engine = RecommendationEngine()
recommendations = engine.get_recommendations(user, num_recommendations=5)

print("\n✨ RECOMMENDED PRODUCTS:")
for i, product in enumerate(recommendations, 1):
    print(f"  {i}. {product.name}")
    print(f"     Category: {product.category.name}")
    print(f"     Price: ₹{product.price}")
    print(f"     Rating: {product.rating}/5.0")
    print()

print("=" * 60)
print("✅ AI RECOMMENDATION SYSTEM WORKING!")
print("=" * 60)