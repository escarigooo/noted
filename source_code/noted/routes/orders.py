from flask import Blueprint, render_template, redirect, url_for, session, request, abort, flash
from noted.models import get_db_connection, User, Order, OrderItem, Product
from noted.services.invoice_service import InvoiceService
from noted.services.email_service import EmailService
import os
from flask import send_file
from datetime import datetime
from decimal import Decimal
from functools import wraps

orders_bp = Blueprint('orders', __name__)

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

@orders_bp.route('/orders/<int:order_id>')
def order_details(order_id):
    """View order details with products, addresses, and invoice information"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # First check if the order belongs to the user
    cursor.execute('''
        SELECT * FROM orders 
        WHERE id = %s AND user_id = %s
    ''', (order_id, user_id))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        connection.close()
        abort(404, "Order not found or you don't have permission to view it")
    
    # Get order items with product details
    cursor.execute('''
        SELECT 
            oi.*,
            p.name AS product_name,
            p.description AS product_description,
            p.image AS product_image
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    ''', (order_id,))
    
    order_items = cursor.fetchall()
    
    # Get shipping address
    cursor.execute('''
        SELECT * FROM shipping_addresses
        WHERE order_id = %s
    ''', (order_id,))
    
    shipping_address = cursor.fetchone()
    
    # Get billing address
    cursor.execute('''
        SELECT * FROM billing_addresses
        WHERE order_id = %s
    ''', (order_id,))
    
    billing_address = cursor.fetchone()
    
    # Get invoice details if available
    cursor.execute('''
        SELECT * FROM invoices
        WHERE order_id = %s
    ''', (order_id,))
    
    invoice = cursor.fetchone()
    
    # Get payment information
    cursor.execute('''
        SELECT * FROM payment_info
        WHERE order_id = %s
    ''', (order_id,))
    
    payment = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # Format dates
    order['formatted_date'] = order['order_date'].strftime('%d %b, %Y')
    
    if invoice and invoice['invoice_date']:
        invoice['formatted_date'] = invoice['invoice_date'].strftime('%d %b, %Y')
    
    if payment and payment['payment_date']:
        payment['formatted_date'] = payment['payment_date'].strftime('%d %b, %Y')
    
    return render_template(
        'pages/account/order_details.html',
        order=order,
        items=order_items,
        shipping=shipping_address,
        billing=billing_address,
        invoice=invoice,
        payment=payment
    )

@orders_bp.route('/orders/<int:order_id>/invoice')
def view_invoice(order_id):
    """View invoice PDF"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Check if the order belongs to the user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT 1 FROM orders
        WHERE id = %s AND user_id = %s
    ''', (order_id, user_id))
    
    order_exists = cursor.fetchone()
    
    if not order_exists:
        cursor.close()
        connection.close()
        abort(403, "You don't have permission to view this invoice")
    
    # Get invoice path
    cursor.execute('''
        SELECT i.pdf_path
        FROM invoices i
        WHERE i.order_id = %s
    ''', (order_id,))
    
    invoice = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not invoice or not invoice.get('pdf_path'):
        abort(404, "Invoice not found")
    
    # Get the full path to the PDF
    pdf_path = os.path.join(os.getcwd(), 'noted/static', invoice['pdf_path'].replace('/static/', ''))
    
    if not os.path.exists(pdf_path):
        abort(404, "Invoice file not found")
    
    # Return the file for viewing in browser
    return send_file(pdf_path, mimetype='application/pdf')

@orders_bp.route('/orders/<int:order_id>/download-invoice')
def download_invoice(order_id):
    """Download invoice PDF"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Check if the order belongs to the user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT 1 FROM orders
        WHERE id = %s AND user_id = %s
    ''', (order_id, user_id))
    
    order_exists = cursor.fetchone()
    
    if not order_exists:
        cursor.close()
        connection.close()
        abort(403, "You don't have permission to download this invoice")
    
    # Get invoice path
    cursor.execute('''
        SELECT i.pdf_path, i.invoice_number
        FROM invoices i
        WHERE i.order_id = %s
    ''', (order_id,))
    
    invoice = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not invoice or not invoice.get('pdf_path'):
        abort(404, "Invoice not found")
    
    # Get the full path to the PDF
    pdf_path = os.path.join(os.getcwd(), 'noted/static', invoice['pdf_path'].replace('/static/', ''))
    
    if not os.path.exists(pdf_path):
        abort(404, "Invoice file not found")
    
    # Return the file for download
    return send_file(
        pdf_path, 
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"noted_invoice_{invoice['invoice_number']}.pdf"
    )

@orders_bp.route('/invoice/<int:order_id>')
def view_invoice_secure(order_id):
    """View invoice for an order with token authentication"""
    from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
    from flask import current_app, abort
    
    # Verify token for security
    token = request.args.get('token')
    if not token:
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        # If logged in, check that this order belongs to the user
        user_id = session['user_id']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT id FROM orders 
            WHERE id = %s AND user_id = %s
        ''', (order_id, user_id))
        
        order = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not order:
            abort(403, "You don't have permission to view this invoice")
    else:
        # Verify the token
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            token_order_id = serializer.loads(
                token, 
                salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'email-salt'),
                max_age=604800  # Valid for 7 days
            )
            if int(token_order_id) != order_id:
                abort(403, "Invalid token for this invoice")
        except (BadSignature, SignatureExpired):
            abort(403, "Invalid or expired token")
    
    # Get invoice path from invoice service
    invoice_service = InvoiceService()
    invoice_path, error = invoice_service.get_invoice_path(order_id)
    
    if error or not invoice_path:
        # If invoice doesn't exist, try to generate it
        invoice_path, error = invoice_service.generate_invoice_pdf(order_id)
        
    if error or not invoice_path:
        abort(404, f"Invoice not found: {error}")
    
    return send_file(
        invoice_path,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=f'invoice_{order_id}.pdf'
    )

@orders_bp.route('/orders/<int:order_id>/send-confirmation')
def send_order_confirmation(order_id):
    """Manually send order confirmation email (for testing)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Check if order belongs to user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT o.*, u.name as user_name, u.email as user_email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = %s AND o.user_id = %s
    ''', (order_id, user_id))
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not result:
        abort(404, "Order not found")
    
    # Create a simple order object with the data
    class SimpleOrder:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    order = SimpleOrder(result)
    
    # Send confirmation email
    success = EmailService.send_order_email(
        user_email=result['user_email'],
        user_name=result['user_name'],
        order=order,
        email_type='confirmation',
        include_invoice=True
    )
    
    if success:
        return f"Order confirmation email sent successfully to {result['user_email']}"
    else:
        return "Failed to send order confirmation email", 500

@orders_bp.route('/orders/<int:order_id>/send-status-update')
def send_order_status_update(order_id):
    """Manually send order status update email (for testing)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Check if order belongs to user
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT o.*, u.name as user_name, u.email as user_email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = %s AND o.user_id = %s
    ''', (order_id, user_id))
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not result:
        abort(404, "Order not found")
    
    # Create a simple order object with the data
    class SimpleOrder:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    order = SimpleOrder(result)
    
    # Send status update email
    success = EmailService.send_order_email(
        user_email=result['user_email'],
        user_name=result['user_name'],
        order=order,
        email_type='status_update',
        include_invoice=False
    )
    
    if success:
        return f"Order status update email sent successfully to {result['user_email']}"
    else:
        return "Failed to send order status update email", 500

@orders_bp.route('/preview-email/<email_type>')
@admin_required
def preview_email(email_type):
    """Preview email templates in the browser with mock data"""
    from datetime import datetime
    
    # Mock user data
    mock_user = {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    # Mock order data
    mock_order = type('MockOrder', (), {
        'id': 12345,
        'status': 'delivered',
        'order_date': datetime.now(),
        'shipping_method': 'standard',
        'total_amount': 75.50,
        'tracking_number': 'NT1234567890',
        'shipping_carrier': 'CTT Expresso'
    })()
    
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
    
    # Calculate totals
    subtotal = sum(Decimal(str(item['unit_price'])) * Decimal(str(item['quantity'])) for item in mock_items)
    shipping_cost = Decimal('5.0')
    tax = subtotal * Decimal('0.23')
    total = subtotal + shipping_cost + tax
    
    # Template and context mapping
    templates = {
        'order_confirmation': {
            'template': 'emails/order_confirmation_with_invoice.html',
            'context': {
                'user': mock_user,
                'order': mock_order,
                'items': mock_items,
                'order_date': mock_order.order_date.strftime("%B %d, %Y"),
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'tax': tax,
                'total': total,
                'invoice_link': '#',
                'related_products': mock_related_products
            }
        },
        'order_status': {
            'template': 'emails/order_status.html',
            'context': {
                'user': mock_user,
                'order': mock_order,
                'items': mock_items,
                'order_date': mock_order.order_date.strftime("%B %d, %Y"),
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'tax': tax,
                'total': total,
                'order_status': mock_order.status,
                'related_products': mock_related_products,
                'tracking_info': {
                    'number': mock_order.tracking_number,
                    'carrier': mock_order.shipping_carrier,
                    'url': f'https://www.ctt.pt/feapl_2/app/open/cttexpresso/objectSearch/objectSearch.jspx?objects={mock_order.tracking_number}'
                }
            }
        },
        'registration': {
            'template': 'emails/registration.html',
            'context': {
                'user_name': mock_user['name'],
                'verification_token': 'mock_token_123',
                'verify_url': '#'
            }
        },
        'password_reset': {
            'template': 'emails/password_reset.html',
            'context': {
                'user_name': mock_user['name'],
                'reset_token': 'mock_reset_token_456',
                'reset_url': '#'
            }
        }
    }
    
    if email_type not in templates:
        abort(404, f"Email type '{email_type}' not found")
    
    template_info = templates[email_type]
    
    # Add standard context variables
    context = template_info['context']
    context.update({
        'now': datetime.now(),
        'company_name': 'noted;',
        'support_email': 'support@noted.pt',
        'site_url': 'https://noted.pt',
        'company_address': 'Rua da Inovação, 123<br>1000-001 Lisboa, Portugal'
    })
    
    return render_template(template_info['template'], **context)

