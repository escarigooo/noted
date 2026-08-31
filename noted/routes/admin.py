from flask import Blueprint, current_app, render_template, session, redirect, url_for, flash, jsonify, request
from functools import wraps
from noted.models import User, db
import os
import json
import glob
import random
from datetime import datetime
from decimal import Decimal
from werkzeug.exceptions import HTTPException
from ..services.email_service import EmailService
from ..models import Order

admin_bp = Blueprint('admin', __name__)
REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Move the admin_required decorator directly into this file
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user = db.session.get(User, session['user_id'])
        if not user or user.role != 1:  # Assuming role 1 is admin
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('misc.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    """
    Main admin dashboard page - simple and minimalist
    Shows overview statistics and quick access to admin functions
    """
    # Get current user from session
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    
    return render_template('pages/admin/dashboard.html', user=user)

@admin_bp.route('/admin/users')
@admin_required  
def users():
    """Users management page"""
    users = User.query.all()
    # Add admin breadcrumbs
    admin_breadcrumbs = [
        {'label': 'users', 'url': None}
    ]
    return render_template('pages/admin/users/users.html', 
                          users=users,
                          admin_breadcrumbs=admin_breadcrumbs)

@admin_bp.route('/admin/categories')
@admin_required
def categories():
    """Categories management page"""
    admin_breadcrumbs = [
        {'label': 'categories', 'url': None}
    ]
    return render_template('pages/admin/categories/categories.html',
                          admin_breadcrumbs=admin_breadcrumbs) 

@admin_bp.route('/admin/products')
@admin_required
def products():
    """Products management page"""
    admin_breadcrumbs = [
        {'label': 'products', 'url': None}
    ]
    return render_template('pages/admin/products/products.html',
                          admin_breadcrumbs=admin_breadcrumbs)

@admin_bp.route('/admin/orders')
@admin_required
def orders():
    """Orders page"""
    admin_breadcrumbs = [
        {'label': 'orders', 'url': None}
    ]
    return render_template('pages/admin/orders/orders.html',
                          admin_breadcrumbs=admin_breadcrumbs)

@admin_bp.route('/admin/analytics') 
@admin_required
def analytics():
    """Analytics page with simple statistics"""
    admin_breadcrumbs = [
        {'label': 'analytics', 'url': None}
    ]
    return render_template('pages/admin/analytics/analytics.html',
                          admin_breadcrumbs=admin_breadcrumbs)


@admin_bp.get('/api/admin/dashboard')
@admin_required
def dashboard_data():
    from noted.services.analytics_service import analytics_data

    return jsonify(analytics_data())


@admin_bp.get('/api/admin/analytics')
@admin_required
def get_analytics_data():
    from noted.services.analytics_service import analytics_data

    return jsonify(analytics_data())


@admin_bp.post('/admin/refresh-analytics')
@admin_required
def refresh_analytics():
    from noted.services.analytics_service import analytics_data

    return jsonify(success=True, data=analytics_data(), source='database')


@admin_bp.get('/api/admin/graphics')
@admin_required
def get_graphics_data():
    from noted.services.analytics_service import graphics_data

    return jsonify(graphics_data())


@admin_bp.post('/admin/refresh-graphics')
@admin_required
def refresh_graphics():
    from noted.services.analytics_service import graphics_data

    return jsonify(success=True, data=graphics_data(), source='database')

@admin_bp.route('/admin/orders/<int:order_id>/invoice')
@admin_required
def view_invoice(order_id):
    """View invoice PDF"""
    from flask import send_file, abort
    from noted.models import get_db_connection
    from noted.services.invoice_service import resolve_invoice_path

    try:
        # Get invoice path from database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT i.pdf_path
            FROM invoices i
            WHERE i.order_id = %s
        ''', (order_id,))
        
        invoice = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not invoice or not invoice.get('pdf_path'):
            # No invoice found
            abort(404, description="Invoice not found")
            
        pdf_path = resolve_invoice_path(invoice['pdf_path'])
        
        if not pdf_path or not os.path.exists(pdf_path):
            # PDF file doesn't exist
            abort(404, description="Invoice file not found")
            
        # Return the file for viewing in browser
        return send_file(pdf_path, mimetype='application/pdf')
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error viewing invoice: {str(e)}")
        abort(500, description="Error retrieving invoice")

@admin_bp.route('/admin/orders/<int:order_id>/print')
@admin_required
def print_order(order_id):
    """Print-friendly version of order"""
    from noted.models import get_db_connection
    from flask import request

    try:
        # Get print options from query string
        print_options = request.args.get('options', '').split(',')
        
        # Get order details
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get order with customer info
        cursor.execute('''
            SELECT 
                o.*,
                u.name AS customer_name,
                u.email AS customer_email
            FROM orders o
            LEFT JOIN users u ON o.user_id = u.id
            WHERE o.id = %s
        ''', (order_id,))
        
        order = cursor.fetchone()
        
        if not order:
            return "Order not found", 404
            
        # Get shipping and billing addresses
        cursor.execute('''
            SELECT * FROM shipping_addresses WHERE order_id = %s
        ''', (order_id,))
        shipping = cursor.fetchone()
        
        cursor.execute('''
            SELECT * FROM billing_addresses WHERE order_id = %s
        ''', (order_id,))
        billing = cursor.fetchone()
        
        # Get order items
        cursor.execute('''
            SELECT 
                oi.*,
                p.name AS product_name,
                p.description AS product_description
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        ''', (order_id,))
        
        order_items = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template('pages/admin/orders/print_order.html',
                              order=order,
                              shipping=shipping,
                              billing=billing,
                              items=order_items,
                              print_options=print_options)
                              
    except Exception as e:
        print(f"Error printing order: {str(e)}")
        return "Error generating print view", 500

@admin_bp.route('/admin/review')
@admin_required
def admin_review_dashboard():
    """Admin dashboard for reviewing all customer-facing aspects of the site"""
    # Get current user from session
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    
    return render_template('pages/admin/review/dashboard.html', user=user)

@admin_bp.route('/admin/review/emails')
@admin_required
def email_dashboard():
    """Show dashboard of all email templates"""
    # Get current user from session
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    
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
    
    return render_template('pages/admin/emails/dashboard.html', templates=template_files, user=user)

@admin_bp.route('/admin/review/emails/data', methods=['GET'])
@admin_required
def get_email_test_data():
    """Return test data for email templates as JSON"""
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
            'image': 'folio.png',
            'image_url': '/static/img/products/folio.png',
            'description': 'Professional leather portfolio for documents'
        },
        {
            'id': 4,
            'name': 'Desk Organizer',
            'price': 28.00,
            'image': 'essentials.png',
            'image_url': '/static/img/products/essentials.png',
            'description': 'Bamboo desk organizer with multiple compartments'
        }
    ]
    
    # Calculate totals (using strings to handle decimal serialization)
    subtotal = str(sum(Decimal(str(item['unit_price'])) * Decimal(str(item['quantity'])) for item in mock_items))
    shipping_cost = '5.0'
    tax = str(Decimal(subtotal) * Decimal('0.23'))
    total = str(Decimal(subtotal) + Decimal(shipping_cost) + Decimal(tax))
    
    # Return all test data
    return jsonify({
        'user': mock_user,
        'order': mock_order,
        'items': mock_items,
        'related_products': mock_related_products,
        'order_date': mock_order['order_date'],
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': total
    })

@admin_bp.route('/admin/reviews')
@admin_required
def reviews():
    """Website reviews and preview center"""
    admin_breadcrumbs = [
        {'label': 'reviews', 'url': None}
    ]
    return render_template('pages/admin/reviews/reviews.html',
                          admin_breadcrumbs=admin_breadcrumbs)

@admin_bp.route('/preview-email/<email_type>')
@admin_required
def preview_email(email_type):
    """Preview email templates with mock data"""
    try:
        # Get mock data based on email type
        if email_type == 'order_confirmation':
            # Create mock order data
            mock_order = type('MockOrder', (), {})()
            mock_order.id = 12345
            mock_order.order_date = datetime.now()
            mock_order.status = 'pending'
            mock_order.shipping_method = 'standard'
            mock_order.first_name = 'John'
            mock_order.last_name = 'Doe'
            mock_order.email = 'john.doe@example.com'
            mock_order.phone = '+351 123 456 789'
            mock_order.street_address = '123 Main Street'
            mock_order.city = 'Lisbon'
            mock_order.zip_code = '1000-000'
            mock_order.country = 'Portugal'
            
            # Mock order items
            mock_items = [
                {
                    'product_name': 'Premium Notebook',
                    'quantity': 2,
                    'unit_price': 15.99,
                    'total_price': 31.98
                },
                {
                    'product_name': 'Sticky Notes Pack',
                    'quantity': 1,
                    'unit_price': 8.50,
                    'total_price': 8.50
                }
            ]
            
            from decimal import Decimal
            subtotal = Decimal('40.48')
            shipping_cost = Decimal('5.00')
            tax = subtotal * Decimal('0.23')
            total = subtotal + shipping_cost + tax
            
            return render_template('emails/order_confirmation.html',
                user_name='John Doe',
                order=mock_order,
                items=mock_items,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax=tax,
                total=total,
                app_name="noted;",
                support_email="support@example.com"
            )
            
        elif email_type == 'order_status':
            status = request.args.get('status', 'shipped')
            
            # Create mock order data
            mock_order = type('MockOrder', (), {})()
            mock_order.id = 12345
            mock_order.order_date = datetime.now()
            mock_order.status = status
            mock_order.tracking_number = 'CP123456789PT' if status == 'shipped' else None
            mock_order.tracking_url = 'https://www.ctt.pt/tracking/CP123456789PT' if status == 'shipped' else None
            mock_order.shipping_carrier = 'CTT' if status == 'shipped' else None
            
            # Mock order items
            mock_items = [
                {
                    'product_name': 'Premium Notebook',
                    'quantity': 2,
                    'unit_price': 15.99,
                    'total_price': 31.98
                }
            ]
            
            from decimal import Decimal
            subtotal = Decimal('31.98')
            shipping_cost = Decimal('5.00')
            tax = subtotal * Decimal('0.23')
            total = subtotal + shipping_cost + tax
            
            return render_template('emails/order_status.html',
                user_name='John Doe',
                order=mock_order,
                order_status=status,
                items=mock_items,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax=tax,
                total=total,
                app_name="noted;",
                support_email="support@example.com"
            )
            
        elif email_type == 'registration':
            return render_template('emails/registration.html',
                user_name='John Doe',
                verification_link='http://localhost:5000/verify/abc123',
                app_name="noted;",
                support_email="support@example.com"
            )
            
        elif email_type == 'password_reset':
            return render_template('emails/password_reset.html',
                user_name='John Doe',
                reset_link='http://localhost:5000/reset-password/abc123',
                app_name="noted;",
                support_email="support@example.com"
            )
            
        elif email_type == 'invoice_email':
            # Similar to order confirmation but with invoice
            mock_order = type('MockOrder', (), {})()
            mock_order.id = 12345
            mock_order.order_date = datetime.now()
            mock_order.status = 'pending'
            mock_order.invoice_number = 'INV-2025-001'
            
            mock_items = [
                {
                    'product_name': 'Premium Notebook',
                    'quantity': 2,
                    'unit_price': 15.99,
                    'total_price': 31.98
                }
            ]
            
            from decimal import Decimal
            subtotal = Decimal('31.98')
            shipping_cost = Decimal('5.00')
            tax = subtotal * Decimal('0.23')
            total = subtotal + shipping_cost + tax
            
            return render_template('emails/order_confirmation_with_invoice.html',
                user_name='John Doe',
                order=mock_order,
                items=mock_items,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                tax=tax,
                total=total,
                app_name="noted;",
                support_email="support@example.com",
                invoice_link='#'
            )
        
        else:
            return "Email type not found", 404
            
    except Exception as e:
        current_app.logger.error(f"Error previewing email {email_type}: {str(e)}")
        return f"Error loading email preview: {str(e)}", 500

@admin_bp.route('/send-test-email', methods=['POST'])
@admin_required
def send_test_email():
    """Send test email to admin"""
    try:
        data = request.get_json()
        email_type = data.get('email_type')
        status = data.get('status')
        
        # Get current admin user email
        admin_email = session.get('user_email', 'admin@example.com')
        admin_name = session.get('user_name', 'Admin')
        
        # Create mock order for testing
        mock_order = type('MockOrder', (), {})()
        mock_order.id = random.randint(10000, 99999)
        mock_order.order_date = datetime.now()
        mock_order.status = status or 'pending'
        mock_order.shipping_method = 'standard'
        
        success = False
        
        if email_type == 'order_confirmation':
            success = EmailService.send_order_email(
                user_email=admin_email,
                user_name=admin_name,
                order=mock_order,
                email_type='confirmation',
                include_invoice=False
            )
        elif email_type == 'order_status':
            mock_order.status = status or 'shipped'
            success = EmailService.send_order_email(
                user_email=admin_email,
                user_name=admin_name,
                order=mock_order,
                email_type='status_update'
            )
        elif email_type == 'registration':
            success = EmailService.send_registration_email(
                user_email=admin_email,
                user_name=admin_name
            )
        elif email_type == 'password_reset':
            success = EmailService.send_password_reset_email(
                user_email=admin_email,
                user_name=admin_name
            )
        
        if success:
            return jsonify({'success': True, 'message': 'Test email sent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send test email'})
            
    except Exception as e:
        current_app.logger.error(f"Error sending test email: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})
