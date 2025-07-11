import os
import sys
from datetime import datetime
import jinja2
from flask import current_app, url_for
from ..models import get_db_connection
from decimal import Decimal

class InvoiceService:
    """Service for generating and managing invoices"""
    
    def __init__(self):
        import os
        from flask import current_app
        
        # Define multiple possible template paths
        template_paths = [
            os.path.join(current_app.root_path, 'templates', 'emails', 'invoices'),  # Absolute path
            os.path.join('noted', 'templates', 'emails', 'invoices'),                # Relative path
            os.path.join('templates', 'emails', 'invoices')                         # Direct path
        ]
        
        # Log the paths we're checking
        print(f"[DEBUG] Checking template paths: {template_paths}")
        
        # Create a FileSystemLoader that checks multiple paths
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_paths)
        )
        
    def generate_invoice_pdf(self, order_id):
        """Generate PDF invoice for an order"""
        try:
            # Check if invoice already exists
            existing_invoice_path = self.get_invoice_path(order_id)
            if existing_invoice_path:
                return existing_invoice_path, None
            
            # Get order data with all necessary details
            order_data = self._get_order_data(order_id)
            if not order_data:
                return None, "Order not found"
            
            # Check if template exists and can be found
            try:
                template = self.template_env.get_template('invoice_template.html')
                print(f"[DEBUG] Found invoice template successfully")
            except jinja2.exceptions.TemplateNotFound:
                # Template not found, try to create it from a basic template
                print(f"[DEBUG] Template not found, creating a basic template")
                self._create_basic_invoice_template()
                
                # Try to get the template again
                try:
                    template = self.template_env.get_template('invoice_template.html')
                except jinja2.exceptions.TemplateNotFound as e:
                    return None, f"Invoice template not found: {str(e)}. Please create an invoice_template.html file in templates/emails/invoices directory."
            
            # Generate HTML content from template
            html_content = template.render(**order_data)
            
            # Ensure the invoices directory exists in static folder
            try:
                invoices_dir = os.path.join(current_app.static_folder, 'invoices')
                if not os.path.exists(invoices_dir):
                    print(f"[DEBUG] Creating invoices directory: {invoices_dir}")
                    os.makedirs(invoices_dir)
            except Exception as e:
                print(f"[ERROR] Failed to create invoices directory: {str(e)}")
                # Try an alternate location
                alternate_dir = os.path.join(current_app.root_path, 'static', 'invoices')
                print(f"[DEBUG] Trying alternate directory: {alternate_dir}")
                if not os.path.exists(alternate_dir):
                    os.makedirs(alternate_dir)
                invoices_dir = alternate_dir
                
            # Generate PDF file path
            invoice_filename = f"invoice_{order_data['invoice_number'].replace('-', '_')}.pdf"
            pdf_path = os.path.join(invoices_dir, invoice_filename)
            
            # Try multiple PDF generation methods
            success = False
            error_messages = []
            
            # Method 1: Try pdfkit
            try:
                import pdfkit
                pdfkit.from_string(html_content, pdf_path)
                success = True
            except ImportError:
                error_messages.append("pdfkit module not installed. Run 'pip install pdfkit' and ensure wkhtmltopdf is installed.")
            except Exception as e:
                error_messages.append(f"pdfkit error: {str(e)}")
            
            # Method 2: Try WeasyPrint if pdfkit fails
            if not success:
                try:
                    from weasyprint import HTML
                    HTML(string=html_content).write_pdf(pdf_path)
                    success = True
                except ImportError:
                    error_messages.append("WeasyPrint module not installed. Run 'pip install WeasyPrint'.")
                except Exception as e:
                    error_messages.append(f"WeasyPrint error: {str(e)}")
            
            # Method 3: Try ReportLab if both fail
            if not success:
                try:
                    from reportlab.pdfgen import canvas
                    from reportlab.lib.pagesizes import letter
                    # This is a simplified fallback that won't look as good
                    c = canvas.Canvas(pdf_path, pagesize=letter)
                    c.drawString(100, 750, f"Invoice #{order_data['invoice_number']}")
                    c.drawString(100, 730, f"Date: {order_data['invoice_date']}")
                    c.drawString(100, 710, f"Customer: {order_data['customer']['name']}")
                    y = 690
                    for item in order_data['items']:
                        y -= 20
                        c.drawString(100, y, f"{item['name']} x{item['quantity']} - ${item['total']:.2f}")
                    c.drawString(100, y-40, f"Total: ${order_data['total']:.2f}")
                    c.save()
                    success = True
                except ImportError:
                    error_messages.append("ReportLab module not installed. Run 'pip install reportlab'.")
                except Exception as e:
                    error_messages.append(f"ReportLab error: {str(e)}")
            
            if not success:
                return None, "PDF generation failed. Errors: " + "; ".join(error_messages)
            
            # Update invoice record with PDF path
            self._update_invoice_pdf_path(order_id, f"/static/invoices/{invoice_filename}")
            
            return pdf_path, None
            
        except Exception as e:
            print(f"Error generating invoice PDF: {str(e)}")
            return None, str(e)
            
    def _get_order_data(self, order_id):
        """Get all order data needed for invoice generation"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get order details with all related information
        cursor.execute('''
            SELECT 
                o.*,
                u.name AS customer_name,
                u.email AS customer_email,
                sa.first_name AS shipping_first_name,
                sa.last_name AS shipping_last_name,
                sa.street_address AS shipping_street,
                sa.city AS shipping_city,
                sa.state AS shipping_state,
                sa.zip_code AS shipping_zip,
                sa.country AS shipping_country,
                ba.first_name AS billing_first_name,
                ba.last_name AS billing_last_name,
                ba.street_address AS billing_street,
                ba.city AS billing_city,
                ba.state AS billing_state,
                ba.zip_code AS billing_zip,
                ba.country AS billing_country,
                i.invoice_number,
                i.invoice_date,
                i.company_name,
                i.company_vat,
                i.company_address,
                i.payment_terms
            FROM orders o
            LEFT JOIN users u ON o.user_id = u.id
            LEFT JOIN shipping_addresses sa ON o.id = sa.order_id
            LEFT JOIN billing_addresses ba ON o.id = ba.order_id
            LEFT JOIN invoices i ON o.id = i.order_id
            WHERE o.id = %s
        ''', (order_id,))
        
        order = cursor.fetchone()
        if not order:
            cursor.close()
            connection.close()
            return None
            
        # Get order items with product details
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
        
        # Calculate totals if not available
        if not order['subtotal']:
            subtotal = sum(item['unit_price'] * item['quantity'] for item in order_items)
        else:
            subtotal = order['subtotal']
            
        if not order['tax_amount']:
            tax_rate = order['tax_rate'] or 23.0  # Default to Portuguese VAT
            tax_amount = subtotal * (tax_rate / 100)
        else:
            tax_amount = order['tax_amount']
            tax_rate = order['tax_rate']
        
        shipping_cost = Decimal(str(order['shipping_cost'] or '0'))
        discount_amount = Decimal(str(order['discount_amount'] or '0'))
        
        total = subtotal + tax_amount + shipping_cost - discount_amount
        
        # Format the data for the template
        formatted_order = {
            'order_id': order['id'],
            'order_date': order['order_date'].strftime('%d/%m/%Y'),
            'invoice_number': order['invoice_number'],
            'invoice_date': order['invoice_date'].strftime('%d/%m/%Y') if order['invoice_date'] else datetime.now().strftime('%d/%m/%Y'),
            'customer': {
                'name': order['customer_name'],
                'email': order['customer_email']
            },
            'shipping_address': {
                'name': f"{order['shipping_first_name']} {order['shipping_last_name']}",
                'street': order['shipping_street'],
                'city': order['shipping_city'],
                'state': order['shipping_state'],
                'zip': order['shipping_zip'],
                'country': order['shipping_country']
            },
            'billing_address': {
                'name': f"{order['billing_first_name']} {order['billing_last_name']}",
                'street': order['billing_street'],
                'city': order['billing_city'],
                'state': order['billing_state'],
                'zip': order['billing_zip'],
                'country': order['billing_country']
            },
            'items': [{
                'name': item['product_name'],
                'description': item['product_description'],
                'quantity': item['quantity'],
                'unit_price': float(item['unit_price']),
                'total': float(item['unit_price'] * item['quantity'])
            } for item in order_items],
            'subtotal': float(subtotal),
            'tax_rate': float(tax_rate),
            'tax_amount': float(tax_amount),
            'shipping_cost': float(shipping_cost),
            'discount_amount': float(discount_amount),
            'total': float(total),
            'payment_method': order['payment_method'],
            'company': {
                'name': order['company_name'],
                'vat': order['company_vat'],
                'address': order['company_address'],
                'payment_terms': order['payment_terms']
            }
        }
        
        return formatted_order
        
    def _update_invoice_pdf_path(self, order_id, pdf_path):
        """Update the invoice record with the generated PDF path, or create a new invoice record if one doesn't exist"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if invoice record exists
        cursor.execute('SELECT id FROM invoices WHERE order_id = %s', (order_id,))
        invoice = cursor.fetchone()
        
        if invoice:
            # Update existing invoice record
            cursor.execute('''
                UPDATE invoices
                SET pdf_path = %s
                WHERE order_id = %s
            ''', (pdf_path, order_id))
        else:
            # Get order information for creating a new invoice
            cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
            order = cursor.fetchone()
            
            if not order:
                cursor.close()
                connection.close()
                return False
            
            # Generate invoice number based on order
            current_year = datetime.now().year
            invoice_number = f"INV-{current_year}-{order_id:04d}"
            
            # Create new invoice record
            cursor.execute('''
                INSERT INTO invoices (
                    order_id, invoice_number, invoice_date, pdf_path, 
                    company_name, company_vat, company_address, payment_terms
                ) VALUES (
                    %s, %s, CURRENT_TIMESTAMP, %s,
                    'noted; Inc.', 'PT123456789', 'Av. da Liberdade, 1000, Lisboa, Portugal', 'Due on receipt'
                )
            ''', (order_id, invoice_number, pdf_path))
            
            print(f"[DEBUG] Created new invoice record: {invoice_number} for order {order_id}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    def send_invoice_email(self, order_id):
        """Send invoice email with PDF attachment"""
        from .email_service import EmailService
        
        try:
            # Get order and customer data
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute('''
                SELECT 
                    o.id,
                    o.invoice_number,
                    u.name AS customer_name,
                    u.email AS customer_email,
                    i.pdf_path
                FROM orders o
                JOIN users u ON o.user_id = u.id
                JOIN invoices i ON o.id = i.order_id
                WHERE o.id = %s
            ''', (order_id,))
            
            order = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if not order or not order['pdf_path']:
                return False, "Invoice not found or PDF not generated"
            
            # Use the static method for sending invoice emails
            success, message = EmailService.send_invoice_email(
                order['customer_email'],
                order['customer_name'],
                order['id'],
                order['invoice_number'],
                order['pdf_path']
            )
            
            # Update database if email sent successfully
            if success:
                connection = get_db_connection()
                cursor = connection.cursor()
                
                # Update orders table
                cursor.execute('''
                    UPDATE orders
                    SET invoice_sent = TRUE, invoice_sent_date = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (order_id,))
                
                # Create email notification record
                cursor.execute('''
                    INSERT INTO email_notifications 
                    (order_id, notification_type, recipient_email, subject, sent_at, status, attachments)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
                ''', (
                    order_id,
                    'invoice',
                    order['customer_email'],
                    f"noted; - Your Invoice #{order['invoice_number']}",
                    'sent',
                    order['pdf_path']
                ))
                
                connection.commit()
                cursor.close()
                connection.close()
                
            return success, message
            
            # Update database if email sent successfully
            if success:
                connection = get_db_connection()
                cursor = connection.cursor()
                
                # Update orders table
                cursor.execute('''
                    UPDATE orders
                    SET invoice_sent = TRUE, invoice_sent_date = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (order_id,))
                
                # Create email notification record
                cursor.execute('''
                    INSERT INTO email_notifications 
                    (order_id, notification_type, recipient_email, subject, sent_at, status, attachments)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
                ''', (
                    order_id,
                    'invoice',
                    order['customer_email'],
                    subject,
                    'sent',
                    order['pdf_path']
                ))
                
                connection.commit()
                cursor.close()
                connection.close()
                
            return success, message
                
        except Exception as e:
            print(f"Error sending invoice email: {str(e)}")
            return False, str(e)
            
    def get_invoice_path(self, order_id):
        """
        Get the path to an existing invoice PDF if it exists
        
        Args:
            order_id (int): Order ID
            
        Returns:
            tuple: (path, error) where path is the invoice path if successful, and error is any error message
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute('''
                SELECT 
                    pdf_path,
                    invoice_number
                FROM invoices
                WHERE order_id = %s AND pdf_path IS NOT NULL
            ''', (order_id,))
            
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result and result['pdf_path'] and os.path.exists(result['pdf_path']):
                return result['pdf_path'], None
            elif result:
                return None, "Invoice file not found on disk"
            else:
                return None, "Invoice not found in database"
                
        except Exception as e:
            return None, f"Error retrieving invoice: {str(e)}"
        
    def get_invoice_details(self, order_id):
        """
        Get details about an invoice
        
        Args:
            order_id (int): Order ID
            
        Returns:
            dict or None: Dictionary with invoice details if it exists
        """
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT 
                i.*,
                o.status AS order_status,
                o.invoice_sent,
                o.invoice_sent_date,
                u.name AS customer_name,
                u.email AS customer_email
            FROM invoices i
            JOIN orders o ON i.order_id = o.id
            JOIN users u ON o.user_id = u.id
            WHERE i.order_id = %s
        ''', (order_id,))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return result
    
    def _create_basic_invoice_template(self):
        """Create a basic invoice template if none exists"""
        try:
            import os
            from flask import current_app
            
            # Determine the template directory path
            template_dir = os.path.join(current_app.root_path, 'templates', 'emails', 'invoices')
            
            # Create directory if it doesn't exist
            if not os.path.exists(template_dir):
                print(f"[DEBUG] Creating template directory: {template_dir}")
                os.makedirs(template_dir)
            
            # Define a basic invoice template
            basic_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Invoice #{{ invoice_number }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
            color: #333;
            line-height: 1.5;
        }
        .invoice-header {
            border-bottom: 1px solid #ddd;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        .invoice-header h1 {
            margin: 0;
            color: #000;
        }
        .row {
            display: flex;
            margin-bottom: 20px;
        }
        .col {
            flex: 1;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            text-align: left;
            padding: 10px;
            background: #f9f9f9;
            border-bottom: 2px solid #ddd;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .total-row td {
            border-top: 2px solid #000;
            border-bottom: none;
            font-weight: bold;
        }
        .company-info {
            margin-top: 50px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="invoice-header">
        <h1>Invoice #{{ invoice_number }}</h1>
        <p>Date: {{ invoice_date }}</p>
    </div>
    
    <div class="row">
        <div class="col">
            <h3>Bill To:</h3>
            <p>
                {{ customer.name }}<br>
                {{ customer.email }}<br>
                {% if billing_address %}
                {{ billing_address.street }}<br>
                {{ billing_address.city }}, {{ billing_address.state }} {{ billing_address.zip }}<br>
                {{ billing_address.country }}
                {% endif %}
            </p>
        </div>
        <div class="col">
            <h3>Ship To:</h3>
            <p>
                {% if shipping_address %}
                {{ shipping_address.name }}<br>
                {{ shipping_address.street }}<br>
                {{ shipping_address.city }}, {{ shipping_address.state }} {{ shipping_address.zip }}<br>
                {{ shipping_address.country }}
                {% endif %}
            </p>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Item</th>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ item.description }}</td>
                <td>{{ item.quantity }}</td>
                <td>€{{ "%.2f"|format(item.unit_price) }}</td>
                <td>€{{ "%.2f"|format(item.total) }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="3"></td>
                <td>Subtotal</td>
                <td>€{{ "%.2f"|format(subtotal) }}</td>
            </tr>
            <tr>
                <td colspan="3"></td>
                <td>Tax ({{ tax_rate }}%)</td>
                <td>€{{ "%.2f"|format(tax_amount) }}</td>
            </tr>
            <tr>
                <td colspan="3"></td>
                <td>Shipping</td>
                <td>€{{ "%.2f"|format(shipping_cost) }}</td>
            </tr>
            {% if discount_amount > 0 %}
            <tr>
                <td colspan="3"></td>
                <td>Discount</td>
                <td>-€{{ "%.2f"|format(discount_amount) }}</td>
            </tr>
            {% endif %}
            <tr class="total-row">
                <td colspan="3"></td>
                <td>Total</td>
                <td>€{{ "%.2f"|format(total) }}</td>
            </tr>
        </tbody>
    </table>
    
    <div class="company-info">
        <p><strong>{{ company.name }}</strong><br>
        VAT: {{ company.vat }}<br>
        {{ company.address }}<br>
        Payment Terms: {{ company.payment_terms }}</p>
    </div>
</body>
</html>
"""
            
            # Write the template to file
            template_path = os.path.join(template_dir, 'invoice_template.html')
            print(f"[DEBUG] Writing basic template to: {template_path}")
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(basic_template)
                
            print(f"[DEBUG] Basic invoice template created successfully")
            return True
                
        except Exception as e:
            print(f"[ERROR] Failed to create basic invoice template: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False
