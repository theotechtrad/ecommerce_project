# 🛒 ShopAI - AI-Powered E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Django-based e-commerce platform featuring **AI-powered product recommendations** and **Cython-optimized performance**. Built as a demonstration of hybrid recommendation systems combining content-based and collaborative filtering.

[ShopAI Link]  https://ecommerce777.pythonanywhere.com/

---

## 🌟 **Features**

### Core E-Commerce Functionality
- ✅ Product catalog with categories
- ✅ Advanced search and filtering
- ✅ Shopping cart management
- ✅ Secure checkout process
- ✅ Order tracking
- ✅ User authentication (register/login/logout)

### AI/ML Capabilities
- 🤖 **Hybrid Recommendation Engine**
  - Content-based filtering using product features
  - Collaborative filtering based on user behavior
  - Cosine similarity for product matching
- 📊 **Real-time User Tracking**
  - Product views (weight: 1)
  - Cart additions (weight: 3)
  - Purchases (weight: 5)
  - Likes (weight: 4)
  - Dislikes (weight: -2)
- 🎯 **Personalized Suggestions**
  - Homepage recommendations
  - Similar products on detail pages
  - Cart-based recommendations

### Performance Optimization
- ⚡ **Cython Integration**
  - Optimized similarity calculations
  - 3-5x faster than pure Python
  - Scalable to 1000+ products

---

## 🛠️ **Technology Stack**

| Category | Technologies |
|----------|-------------|
| **Backend** | Django 5.0, Python 3.10+ |
| **Database** | SQLite (Development), PostgreSQL (Production) |
| **Machine Learning** | scikit-learn, NumPy, Pandas |
| **Optimization** | Cython |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Deployment** | PythonAnywhere |

---

## 📦 **Installation**

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Local Setup
```bash
# Clone the repository
git clone https://github.com/theotechtrad/ecommerce_project.git
cd ecommerce_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate database with sample data
python manage.py populate_db

# Run development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

##  **How the AI Works**

### 1. Data Collection
The system tracks every user interaction:
```python
User views Product A → Creates interaction (type: 'view', weight: 1)
User adds to cart    → Creates interaction (type: 'cart', weight: 3)
User purchases       → Creates interaction (type: 'purchase', weight: 5)
User likes product   → Creates interaction (type: 'like', weight: 4)
```

### 2. Feature Extraction
Each product is represented by a feature vector:
- Normalized price (0-1 scale)
- Popularity score (0-1 scale)
- Rating (0-1 scale)
- Category ID

### 3. Recommendation Algorithm

**Content-Based Filtering:**
```python
similarity = cosine_similarity(product_features_A, product_features_B)
# Returns similarity score between 0 and 1
```

**Collaborative Filtering:**
```python
user_preference_score = sum(interaction_weight × similarity_score)
# Recommends products based on user's interaction history
```

### 4. Cold Start Handling
For new users with no interaction history:
```python
recommendations = top_products_by(popularity_score × rating)
```

---

##  **Project Structure**
```
ecommerce_project/
├── ecommerce/              # Main project settings
│   ├── settings.py         # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI config
├── shop/                   # E-commerce app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin configuration
│   ├── recommendation.py  # AI recommendation engine
│   ├── similarity_calc.pyx # Cython optimization
│   └── management/
│       └── commands/
│           └── populate_db.py  # Sample data generator
├── templates/             # HTML templates
│   └── shop/
│       ├── base.html
│       ├── home.html
│       ├── product_list.html
│       ├── product_detail.html
│       ├── cart.html
│       ├── checkout.html
│       └── login.html
├── static/                # Static files (CSS, JS)
├── media/                 # User uploads
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🧪 **Testing the AI**

### Manual Testing Flow

1. **Register a new user**
```
   Username: testuser
   Password: testpass123
```

2. **Generate interactions**
   - Browse 5-10 different products
   - Add 2-3 products to cart
   - Like 1-2 products
   - Complete a purchase

3. **Check recommendations**
   - Go to homepage
   - You'll see "Recommended For You" section
   - Recommendations are based on your interactions!

### Automated Testing

Run the test script:
```bash
python test_ai.py
```

This simulates user behavior and displays AI-generated recommendations.

---

##  **Key Algorithms**

### Cosine Similarity
```python
similarity = (A · B) / (||A|| × ||B||)
```
Measures the angle between product feature vectors.

### Weighted Scoring
```python
recommendation_score = Σ(interaction_weight × similarity)
```
Combines user preferences with product similarity.

### Feature Normalization
```python
normalized_value = (value - min) / (max - min)
```
Ensures all features are on the same scale.

---

## 📈 **Performance Metrics**

| Metric | Value |
|--------|-------|
| Response Time | < 200ms |
| Cython Speedup | 3-5x faster |
| Scalability | 1000+ products |
| Accuracy | Improves with interactions |

---

## 🚀 **Deployment**

### PythonAnywhere

1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Clone repository**
```bash
   git clone https://github.com/theotechtrad/ecommerce_project.git
   cd ecommerce_project
```

3. **Setup virtual environment**
```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
```

4. **Configure settings**
```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```

5. **Deploy**
```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   python manage.py populate_db
```

---

## 📚 **API Documentation**

### Models

**Product**
```python
{
    "id": 1,
    "name": "Wireless Headphones",
    "description": "Premium headphones",
    "price": 2999.00,
    "category": "Electronics",
    "rating": 4.5,
    "stock": 50
}
```

**UserInteraction**
```python
{
    "user": "user123",
    "product": 1,
    "interaction_type": "purchase",
    "timestamp": "2024-12-03T10:30:00Z"
}
```

---

## 🔒 **Security Features**

- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure password hashing (PBKDF2)
- ✅ Session management

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  **Author**

**Your Name**
- GitHub: [@theotechtrad](https://github.com/theotechtrad)
- Email: hv.himanshuyadav@gmail.com
- LinkedIn: https://www.linkedin.com/in/hvhimanshu-yadav/

---

##  **Acknowledgments**

- Django Documentation
- scikit-learn Documentation
- Unsplash for product images
- PythonAnywhere for hosting

---

##  **Future Enhancements**

- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Email notifications
- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Advanced filtering options
- [ ] Mobile app (React Native)
- [ ] Real-time chat support
- [ ] Multi-language support

---

## 📞 **Support**

For issues or questions:
- **Email**: hv.himanshuyadav@gmail.com
- **Issues**: [GitHub Issues](https://github.com/theotechtrad/ecommerce_project/issues)

---

Made by **Himanshu yadav**
