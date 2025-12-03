# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, OrderItem, UserInteraction, Category
from .recommendation import RecommendationEngine
from django.http import JsonResponse

def home(request):
    """Home page with featured products and recommendations"""
    products = Product.objects.all()[:8]
    categories = Category.objects.all()
    
    recommended_products = []
    if request.user.is_authenticated:
        engine = RecommendationEngine()
        recommended_products = engine.get_recommendations(request.user, num_recommendations=6)
    
    context = {
        'products': products,
        'recommended_products': recommended_products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    """Display all products with filtering"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    """Product detail page with similar products"""
    product = get_object_or_404(Product, pk=pk)
    
    # Track product view
    if request.user.is_authenticated:
        UserInteraction.objects.create(
            user=request.user,
            product=product,
            interaction_type='view'
        )
    
    # Get similar products
    engine = RecommendationEngine()
    similar_products = engine.get_similar_products(product.id, num_recommendations=4)
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def add_to_cart(request, pk):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=pk)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Track interaction
    UserInteraction.objects.create(
        user=request.user,
        product=product,
        interaction_type='cart'
    )
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', pk=pk)

@login_required
def cart_view(request):
    """View cart contents"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = cart.get_total()
    
    # Get recommendations based on cart items
    engine = RecommendationEngine()
    cart_product_ids = [item.product.id for item in cart_items]
    recommended_products = engine.get_recommendations(
        request.user, 
        num_recommendations=4,
        exclude_products=cart_product_ids
    )
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'recommended_products': recommended_products,
    }
    return render(request, 'shop/cart.html', context)

@login_required
def update_cart(request, pk):
    """Update cart item quantity"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'remove':
            cart_item.delete()
    
    return redirect('cart')

@login_required
def checkout(request):
    """Checkout process"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        total = cart.get_total()
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )
        
        # Create order items and track purchases
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            # Track purchase interaction
            UserInteraction.objects.create(
                user=request.user,
                product=item.product,
                interaction_type='purchase'
            )
            
            # Update product popularity
            item.product.popularity_score = min(1.0, item.product.popularity_score + 0.05)
            item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_success', order_id=order.id)
    
    total = cart.get_total()
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def order_success(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)

@login_required
def product_feedback(request, pk):
    """Handle product like/dislike feedback"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        feedback_type = request.POST.get('feedback')
        
        if feedback_type in ['like', 'dislike']:
            UserInteraction.objects.create(
                user=request.user,
                product=product,
                interaction_type=feedback_type
            )
            
            messages.success(request, 'Thank you for your feedback!')
        
        return redirect('product_detail', pk=pk)

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Login the user automatically after registration
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created successfully! Welcome {username}!')
            return redirect('home')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'shop/login.html')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')