"""
Email preview and site review dashboard for noted; application
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
import os
import glob
from datetime import datetime
from decimal import Decimal
from functools import wraps
from noted.models import User

email_preview_bp = Blueprint('email_preview', __name__)

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 1:  # Assuming role 1 is admin
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('misc.index'))
        return f(*args, **kwargs)
    return decorated_function

@email_preview_bp.route('/admin/review')
@admin_required
def admin_review_dashboard():
    """Admin dashboard for reviewing all customer-facing aspects of the site"""
    return render_template('pages/admin/review/dashboard.html')

@email_preview_bp.route('/admin/review/emails')
@admin_required
def email_dashboard():
    """Show dashboard of all email templates"""
    # Discover all email templates
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'emails')
    template_files = []
    
    # Find HTML files in email templates directory
    for file in glob.glob(os.path.join(template_dir, '*.html')):
        if os.path.basename(file) != 'base_email.html':  # Skip base template
            template_name = os.path.splitext(os.path.basename(file))[0]
            template_files.append({
                'name': template_name,
                'pretty_name': template_name.replace('_', ' ').title(),
                'path': file,
                'preview_url': f'/preview-email/{template_name}'
            })
    
    # Also find templates in subdirectories
    for dir_path in glob.glob(os.path.join(template_dir, '*/')):
        dir_name = os.path.basename(os.path.normpath(dir_path))
        if dir_name == 'components':  # Skip components directory
            continue
            
        for file in glob.glob(os.path.join(dir_path, '*.html')):
            template_name = f"{dir_name}/{os.path.splitext(os.path.basename(file))[0]}"
            template_files.append({
                'name': template_name,
                'pretty_name': f"{dir_name.title()}: {os.path.splitext(os.path.basename(file))[0].replace('_', ' ').title()}",
                'path': file,
                'preview_url': f'/preview-email/{template_name}'
            })
    
    return render_template('pages/admin/emails/dashboard.html', templates=template_files)

@email_preview_bp.route('/admin/review/emails/data', methods=['GET'])
@admin_required
def get_email_test_data():
    """Return test data for email templates as JSON"""
    from datetime import datetime
    
    # Default test data
    mock_user = {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    # Mock order data
    mock_order = {
        'id': 12345,
        'status': 'delivered',
        'order_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'shipping_method': 'standard',
        'total_amount': 75.50,
        'tracking_number': 'NT1234567890',
        'shipping_carrier': 'CTT Expresso'
    }
    
    # Mock order items
    mock_items = [
        {
            'product_id': 1,
            'product_name': 'Premium Notebook Set',
            'product_description': 'Elegant hardcover notebooks with premium paper',
            'product_image': 'notebook-premium.jpg',
            'quantity': 2,
            'unit_price': 25.00
        },
        {
            'product_id': 2,
            'product_name': 'Designer Pen Collection',
            'product_description': 'Professional writing instruments',
            'product_image': 'pen-collection.jpg',
            'quantity': 1,
            'unit_price': 35.50
        }
    ]
    
    # Mock related products
    mock_related_products = [
        {
            'id': 3,
            'name': 'Leather Portfolio',
            'price': 45.00,
            'image': 'portfolio-leather.jpg',
            'image_url': '/static/img/products/portfolio-leather.jpg',
            'description': 'Professional leather portfolio for documents'
        },
        {
            'id': 4,
            'name': 'Desk Organizer',
            'price': 28.00,
            'image': 'organizer-desk.jpg',
            'image_url': '/static/img/products/organizer-desk.jpg',
            'description': 'Bamboo desk organizer with multiple compartments'
        }
    ]
    
    # Calculate totals (without tax, using strings to handle decimal serialization)
    subtotal = str(sum(Decimal(str(item['unit_price'])) * Decimal(str(item['quantity'])) for item in mock_items))
    shipping_cost = '5.0'
    total = str(Decimal(subtotal) + Decimal(shipping_cost))
    
    # Return all test data
    return jsonify({
        'user': mock_user,
        'order': mock_order,
        'items': mock_items,
        'related_products': mock_related_products,
        'order_date': mock_order['order_date'],
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total
    })

@email_preview_bp.route('/admin/preview-email/<template_name>')
@admin_required
def preview_email_template(template_name):
    """Preview a specific email template with mock data"""
    from flask import request
    
    # Handle order status emails with specific status
    if template_name == 'order_status':
        status = request.args.get('status', 'pending')
        
        # Create mock objects similar to order_confirmation
        class MockOrder:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        class MockProduct:
            def __init__(self, name, features=None):
                self.name = name
                self.features = features or []
        
        class MockItem:
            def __init__(self, product_name, quantity, unit_price):
                self.product = MockProduct(product_name)
                self.quantity = quantity
                self.unit_price = unit_price
        
        # Mock order items
        mock_items = [
            MockItem('Premium Notebook Set', 2, 25.00),
            MockItem('Designer Pen Collection', 1, 25.50)
        ]
        
        # Mock order data for order status emails
        mock_order = MockOrder({
            'id': 12345,
            'status': status,
            'order_date': '2025-07-02 14:30:00',
            'total_amount': 75.50,
            'shipping_method': 'standard',
            'tracking_number': 'CP123456789PT' if status in ['shipped', 'delivered'] else None,
            'items': mock_items  # Add items to the order object
        })
        
        # Calculate totals (without tax)
        subtotal = 75.50
        shipping_cost = 5.00
        total = 80.50
        
        # Add tracking info for shipped orders
        tracking_info = None
        if status == 'shipped':
            tracking_info = {
                'number': 'CP123456789PT',
                'carrier': 'CTT Expresso',
                'url': 'https://www.ctt.pt/tracking'
            }
        
        return render_template('emails/order_status.html',
            user={'name': 'John Doe'},
            order=mock_order,
            items=mock_items,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            tracking_info=tracking_info,
            company_name='noted;',
            support_email='support@noted.com',
            site_url=request.url_root.rstrip('/')
        )
    
    # Handle other email templates
    elif template_name == 'order_confirmation':
        # Create a simple object-like structure for order
        class MockOrder:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        class MockProduct:
            def __init__(self, name, features=None):
                self.name = name
                self.features = features or []
        
        class MockItem:
            def __init__(self, product_name, quantity, unit_price):
                self.product = MockProduct(product_name)
                self.quantity = quantity
                self.unit_price = unit_price
        
        mock_items = [
            MockItem('Premium Notebook', 2, 15.99),
            MockItem('Sticky Notes Pack', 1, 14.01)
        ]
        
        mock_order = MockOrder({
            'id': 12345,
            'order_date': '2025-07-02 14:30:00',
            'total_amount': 45.99,
            'items': mock_items,
            'shipping_address': {
                'first_name': 'John',
                'last_name': 'Doe',
                'street_address': '123 Main Street',
                'city': 'Lisbon',
                'zip_code': '1000-100',
                'country': 'Portugal',
                'phone': '+351 123 456 789'
            },
            'shipping_method': 'standard'
        })
        
        # Calculate totals (without tax)
        subtotal = 45.99
        shipping_cost = 5.00
        total = 50.99
        
        return render_template('emails/order_confirmation.html',
            user={'name': 'John Doe'},
            user_name='John Doe',
            order=mock_order,
            order_date='2025-07-02 14:30:00',
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            company_name='noted;',
            site_url=request.url_root.rstrip('/')
        )
        
    elif template_name == 'registration':
        return render_template('emails/registration.html',
            user={'name': 'John Doe'},
            company_name='noted;',
            site_url=request.url_root.rstrip('/')
        )
        
    elif template_name == 'password_reset':
        return render_template('emails/password_reset.html',
            user={'name': 'John Doe'},
            reset_url=f"{request.url_root}reset-password?token=sample-token",
            company_name='noted;',
            site_url=request.url_root.rstrip('/')
        )
        
    elif template_name == 'invoice_email':
        mock_order = {
            'id': 12345,
            'order_date': '2025-07-02 14:30:00',
            'total_amount': 45.99,
            'invoice_number': 'INV-2025-001'
        }
        
        # Mock order items for the order_summary_table macro
        mock_items = [
            {
                'product_name': 'Premium Notebook',
                'product_description': 'Elegant hardcover notebook with premium paper',
                'product_image': 'notebook-premium.jpg',
                'quantity': 2,
                'unit_price': 15.99
            },
            {
                'product_name': 'Sticky Notes Pack',
                'product_description': 'Colorful sticky notes collection',
                'product_image': 'sticky-notes.jpg',
                'quantity': 1,
                'unit_price': 14.01
            }
        ]
        
        # Calculate totals (without tax)
        subtotal = 31.98
        shipping_cost = 5.00
        total = 36.98
        
        return render_template('emails/order_confirmation_with_invoice.html',
            user={'name': 'John Doe'},
            order=mock_order,
            order_date='2025-07-02 14:30:00',
            items=mock_items,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            invoice_link=f"{request.url_root}invoices/sample-invoice.pdf",
            company_name='noted;',
            site_url=request.url_root.rstrip('/')
        )
    
    else:
        return f"Email template '{template_name}' not found", 404
