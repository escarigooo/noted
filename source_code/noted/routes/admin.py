from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from functools import wraps
from noted.models import User
import os
import json
import glob
from datetime import datetime
from decimal import Decimal
from ..services.email_service import EmailService
from ..models import Order

admin_bp = Blueprint('admin', __name__)

# Move the admin_required decorator directly into this file
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
        user = User.query.get(session['user_id'])
    
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

@admin_bp.route('/admin/refresh-analytics', methods=['POST'])
@admin_required
def refresh_analytics():
    """
    Refresh analytics data - with fallback if notebook execution fails
    """
    try:
        import subprocess
        import sys
        import os
        from datetime import datetime
        
        print("REFRESH Starting analytics refresh process...")
        
        # First, find the existing JSON file for fallback
        possible_json_paths = [
            os.path.join(os.getcwd(), 'noted', 'static', 'data', 'analytics.json'),
            os.path.join(os.getcwd(), 'static', 'data', 'analytics.json'),
            os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'analytics.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'data', 'analytics.json'),
        ]
        
        json_path = None
        for path in possible_json_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                json_path = abs_path
                print(f"FALLBACK Found existing JSON at: {json_path}")
                break
        
        if not json_path:
            return jsonify({
                'success': False,
                'error': 'Analytics JSON file not found',
                'paths_checked': [os.path.abspath(p) for p in possible_json_paths]
            }), 404
            
        # Find the notebook path if we want to try running it
        possible_notebook_paths = [
            os.path.join(os.getcwd(), 'noted', 'notebooks', 'analytics.ipynb'),
            os.path.join(os.getcwd(), 'notebooks', 'analytics.ipynb'),
            os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'analytics.ipynb'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks', 'analytics.ipynb')
        ]
        
        notebook_path = None
        for path in possible_notebook_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                notebook_path = abs_path
                print(f"NOTEBOOK Found at: {notebook_path}")
                break
        
        # Try to find existing JSON file first
        possible_json_paths = [
            os.path.join(os.getcwd(), 'noted', 'static', 'data', 'analytics.json'),
            os.path.join(os.getcwd(), 'static', 'data', 'analytics.json'),
            os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'analytics.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'data', 'analytics.json'),
        ]
        
        json_path = None
        for path in possible_json_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                json_path = abs_path
                print(f"DATA Found existing JSON at: {json_path}")
                break
        
        try:
            # Try to execute the notebook using nbconvert
            print("FAST Attempting to execute notebook...")
            
            # Method 1: Using nbconvert (recommended)
            cmd = [
                sys.executable, '-m', 'jupyter', 'nbconvert', 
                '--execute', 
                '--to', 'notebook',
                '--inplace',
                notebook_path
            ]
            
            print(f"LAUNCH Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout
                cwd=os.path.dirname(notebook_path)  # Run from notebook directory
            )
            
            if result.returncode != 0:
                print(f"FAILED Notebook execution failed!")
                print(f"STDERR: {result.stderr}")
                print(f"STDOUT: {result.stdout}")
                
                # Handle fallback to existing JSON if available
                if json_path:
                    print(f"FALLBACK Using existing JSON file: {json_path}")
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to execute analytics notebook and no existing JSON found',
                        'details': result.stderr,
                        'stdout': result.stdout,
                        'command': ' '.join(cmd)
                    }), 500
        except Exception as e:
            print(f"ERROR Failed to run notebook: {str(e)}")
            # Handle fallback to existing JSON if available
            if not json_path:
                return jsonify({
                    'success': False,
                    'error': f'Failed to execute notebook and no existing JSON found: {str(e)}',
                    'suggestion': 'Install jupyter and nbconvert with: pip install jupyter nbconvert'
                }), 500
        
        print("SUCCESS Notebook executed successfully!")
        print(f"Output: {result.stdout}")
        
        # Try to execute the notebook if found
        notebook_executed = False
        notebook_error = None
        
        if notebook_path:
            try:
                print("FAST Attempting to execute notebook...")
                
                # Using nbconvert to execute the notebook
                cmd = [
                    sys.executable, '-m', 'jupyter', 'nbconvert', 
                    '--execute', 
                    '--to', 'notebook',
                    '--inplace',
                    notebook_path
                ]
                
                print(f"LAUNCH Running command: {' '.join(cmd)}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minute timeout
                    cwd=os.path.dirname(notebook_path)  # Run from notebook directory
                )
                
                if result.returncode == 0:
                    notebook_executed = True
                    print("SUCCESS Notebook executed successfully!")
                else:
                    notebook_error = f"Notebook execution returned non-zero exit code: {result.returncode}"
                    print(f"FAILED {notebook_error}")
                    print(f"STDERR: {result.stderr}")
            except Exception as e:
                notebook_error = str(e)
                print(f"ERROR Failed to run notebook: {notebook_error}")
        else:
            notebook_error = "Notebook not found"
        
        # Read the fresh data
        with open(json_path, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        print(f"CHART Fresh data loaded: {updated_data}")
        
        return jsonify({
            'success': True,
            'data': updated_data,
            'message': 'Analytics data refreshed successfully from database via notebook',
            'notebook_executed': True,
            'notebook_path': notebook_path,
            'json_path': json_path,
            'execution_time': datetime.now().isoformat()
        })
        
        # Read the JSON file - whether it's freshly generated or existing
        with open(json_path, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        response = {
            'success': True,
            'data': updated_data,
            'execution_time': datetime.now().isoformat()
        }
        
        # Add appropriate status messages
        if notebook_executed:
            response['message'] = 'Analytics data refreshed successfully from database via notebook'
            response['notebook_executed'] = True
            response['notebook_path'] = notebook_path
        else:
            response['message'] = 'Using existing analytics data (fallback)'
            response['notebook_executed'] = False
            if notebook_error:
                response['notebook_error'] = notebook_error
                response['suggestion'] = 'To enable automatic analytics updates, install Jupyter: pip install jupyter nbconvert'
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@admin_bp.route('/admin/refresh-graphics', methods=['POST'])
@admin_required
def refresh_graphics():
    """
    Execute the graphics notebook and return updated chart data
    """
    try:
        import subprocess
        import sys
        import os
        from datetime import datetime
        
        print("REFRESH Starting graphics refresh from notebook...")
        
        # Find the notebook path
        possible_notebook_paths = [
            os.path.join(os.getcwd(), 'noted', 'notebooks', 'graphics.ipynb'),
            os.path.join(os.getcwd(), 'notebooks', 'graphics.ipynb'),
            os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'graphics.ipynb'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks', 'graphics.ipynb')
        ]
        
        notebook_path = None
        for path in possible_notebook_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                notebook_path = abs_path
                print(f" Found graphics notebook at: {notebook_path}")
                break
        
        if not notebook_path:
            return jsonify({
                'success': False,
                'error': 'Graphics notebook not found',
                'paths_checked': [os.path.abspath(p) for p in possible_notebook_paths]
            }), 404
        
        # Execute the notebook using nbconvert
        print("FAST Executing graphics notebook...")
        
        cmd = [
            sys.executable, '-m', 'jupyter', 'nbconvert', 
            '--execute', 
            '--to', 'notebook',
            '--inplace',
            notebook_path
        ]
        
        print(f"LAUNCH Running command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            cwd=os.path.dirname(notebook_path)  # Run from notebook directory
        )
        
        if result.returncode != 0:
            print(f"FAILED Graphics notebook execution failed!")
            print(f"STDERR: {result.stderr}")
            print(f"STDOUT: {result.stdout}")
            
            return jsonify({
                'success': False,
                'error': 'Failed to execute graphics notebook',
                'details': result.stderr,
                'stdout': result.stdout,
                'command': ' '.join(cmd)
            }), 500
        
        print("SUCCESS Graphics notebook executed successfully!")
        print(f"Output: {result.stdout}")
        
        # Find and read the updated JSON file
        possible_json_paths = [
            os.path.join(os.getcwd(), 'noted', 'static', 'data', 'graphics.json'),
            os.path.join(os.getcwd(), 'static', 'data', 'graphics.json'),
            os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'graphics.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'data', 'graphics.json'),
            # Also check relative to notebook location
            os.path.join(os.path.dirname(notebook_path), '..', 'static', 'data', 'graphics.json'),
        ]
        
        json_path = None
        for path in possible_json_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                json_path = abs_path
                print(f"DATA Found graphics JSON at: {json_path}")
                break
        
        if not json_path:
            return jsonify({
                'success': False,
                'error': 'Graphics JSON file not found after notebook execution',
                'paths_checked': [os.path.abspath(p) for p in possible_json_paths],
                'notebook_output': result.stdout
            }), 500
        
        # Read the fresh chart data
        with open(json_path, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        print(f"CHART Fresh graphics data loaded with keys: {list(updated_data.keys())}")
        
        return jsonify({
            'success': True,
            'data': updated_data,
            'message': 'Graphics data refreshed successfully from database via notebook',
            'notebook_executed': True,
            'notebook_path': notebook_path,
            'json_path': json_path,
            'execution_time': datetime.now().isoformat()
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Graphics notebook execution timed out (>2 minutes)',
            'suggestion': 'Check database connection or optimize notebook performance'
        }), 500
        
    except FileNotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'Jupyter not found. Please install with: pip install jupyter nbconvert',
            'details': str(e)
        }), 500
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@admin_bp.route('/admin/orders/<int:order_id>/invoice')
@admin_required
def view_invoice(order_id):
    """View invoice PDF"""
    from flask import send_file, abort
    from noted.models import get_db_connection
    import os

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
            
        # Get the full path to the PDF
        pdf_path = os.path.join(os.getcwd(), 'noted/static', invoice['pdf_path'].replace('/static/', ''))
        
        if not os.path.exists(pdf_path):
            # PDF file doesn't exist
            abort(404, description="Invoice file not found")
            
        # Return the file for viewing in browser
        return send_file(pdf_path, mimetype='application/pdf')
        
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
        user = User.query.get(session['user_id'])
    
    return render_template('pages/admin/review/dashboard.html', user=user)

@admin_bp.route('/admin/review/emails')
@admin_required
def email_dashboard():
    """Show dashboard of all email templates"""
    # Get current user from session
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
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
                support_email="support@noted.com"
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
                support_email="support@noted.com"
            )
            
        elif email_type == 'registration':
            return render_template('emails/registration.html',
                user_name='John Doe',
                verification_link='https://noted.com/verify/abc123',
                app_name="noted;",
                support_email="support@noted.com"
            )
            
        elif email_type == 'password_reset':
            return render_template('emails/password_reset.html',
                user_name='John Doe',
                reset_link='https://noted.com/reset-password/abc123',
                app_name="noted;",
                support_email="support@noted.com"
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
                support_email="support@noted.com",
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
        admin_email = session.get('user_email', 'admin@noted.com')
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
