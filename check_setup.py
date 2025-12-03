# check_setup.py
# Run this script to verify your setup is correct
# Usage: python check_setup.py

import os
import sys

def print_status(message, status):
    """Print colored status message"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    required = (3, 8)
    status = version >= required
    print_status(
        f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.8+)",
        status
    )
    return status

def check_file_exists(filepath, description):
    """Check if file exists"""
    status = os.path.exists(filepath)
    print_status(f"{description}: {filepath}", status)
    return status

def check_directory_exists(dirpath, description):
    """Check if directory exists"""
    status = os.path.isdir(dirpath)
    print_status(f"{description}: {dirpath}", status)
    return status

def check_imports():
    """Check required Python packages"""
    packages = {
        'django': 'Django',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print_status(f"{name} installed", True)
        except ImportError:
            print_status(f"{name} NOT installed", False)
            all_ok = False
    
    return all_ok

def check_cython():
    """Check Cython and compiled modules"""
    try:
        import Cython
        print_status("Cython installed", True)
        
        # Check for compiled module
        compiled_files = []
        if os.path.exists('shop'):
            for file in os.listdir('shop'):
                if file.startswith('similarity_calc') and (file.endswith('.pyd') or file.endswith('.so')):
                    compiled_files.append(file)
        
        if compiled_files:
            print_status(f"Cython module compiled: {', '.join(compiled_files)}", True)
            return True
        else:
            print_status("Cython module NOT compiled (run: python setup.py build_ext --inplace)", False)
            return False
    except ImportError:
        print_status("Cython NOT installed", False)
        return False

def check_database():
    """Check database"""
    if os.path.exists('db.sqlite3'):
        print_status("Database file exists", True)
        
        # Try to check if tables exist
        try:
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
            django.setup()
            
            from shop.models import Product, Category
            product_count = Product.objects.count()
            category_count = Category.objects.count()
            
            print_status(f"Products in database: {product_count}", product_count > 0)
            print_status(f"Categories in database: {category_count}", category_count > 0)
            
            if product_count == 0:
                print("  💡 Run: python manage.py populate_db")
            
            return True
        except Exception as e:
            print_status(f"Database tables not created: {e}", False)
            print("  💡 Run: python manage.py migrate")
            return False
    else:
        print_status("Database NOT created", False)
        print("  💡 Run: python manage.py migrate")
        return False

def main():
    """Main check function"""
    print("=" * 60)
    print("🔍 E-Commerce AI Project Setup Checker")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Check Python version
    print("1️⃣  Checking Python Version:")
    all_checks.append(check_python_version())
    print()
    
    # Check project structure
    print("2️⃣  Checking Project Structure:")
    all_checks.append(check_file_exists('manage.py', 'Django manage.py'))
    all_checks.append(check_directory_exists('ecommerce', 'Project directory'))
    all_checks.append(check_directory_exists('shop', 'Shop app directory'))
    all_checks.append(check_directory_exists('templates', 'Templates directory'))
    all_checks.append(check_directory_exists('templates/shop', 'Shop templates'))
    all_checks.append(check_directory_exists('static', 'Static directory'))
    all_checks.append(check_directory_exists('media', 'Media directory'))
    print()
    
    # Check important files
    print("3️⃣  Checking Important Files:")
    all_checks.append(check_file_exists('shop/models.py', 'Models file'))
    all_checks.append(check_file_exists('shop/views.py', 'Views file'))
    all_checks.append(check_file_exists('shop/urls.py', 'URLs file'))
    all_checks.append(check_file_exists('shop/admin.py', 'Admin file'))
    all_checks.append(check_file_exists('shop/recommendation.py', 'Recommendation engine'))
    all_checks.append(check_file_exists('shop/similarity_calc.pyx', 'Cython file'))
    all_checks.append(check_file_exists('setup.py', 'Setup file'))
    all_checks.append(check_file_exists('templates/shop/base.html', 'Base template'))
    all_checks.append(check_file_exists('templates/shop/home.html', 'Home template'))
    all_checks.append(check_file_exists('requirements.txt', 'Requirements file'))
    print()
    
    # Check Python packages
    print("4️⃣  Checking Python Packages:")
    all_checks.append(check_imports())
    print()
    
    # Check Cython
    print("5️⃣  Checking Cython:")
    cython_ok = check_cython()
    if not cython_ok:
        print("  ⚠️  Cython not compiled - app will use slower Python fallback")
    print()
    
    # Check database
    print("6️⃣  Checking Database:")
    all_checks.append(check_database())
    print()
    
    # Final summary
    print("=" * 60)
    if all(all_checks):
        print("✅ All critical checks passed! You're ready to go!")
        print()
        print("Next steps:")
        print("1. python manage.py runserver")
        print("2. Visit http://127.0.0.1:8000")
        print("3. Register a user and test the features")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("Quick fixes:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Run migrations: python manage.py migrate")
        print("3. Populate database: python manage.py populate_db")
        print("4. Build Cython (optional): python setup.py build_ext --inplace")
    print("=" * 60)

if __name__ == '__main__':
    main()