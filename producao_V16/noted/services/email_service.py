"""
Email service module for sending various types of emails
"""
from flask import current_app, render_template, url_for
from flask_mail import Message
import logging
import os
import json
import traceback
from datetime import datetime
from decimal import Decimal
from ..models import get_db_connection

class EmailService:
    """Service class for handling all email operations"""

    @staticmethod
    def send_email(to, subject, template, context=None, attachments=None):
        """
        Send an email using Flask-Mail with template and optional attachments
        
        Args:
            to (str or list): Recipient email address(es)
            subject (str): Email subject
            template (str): Path to email template
            context (dict): Template variables
            attachments (list): List of attachment dicts with keys:
                - path: File path
                - filename: Name to use in email
                - content_type: MIME type (defaults to 'application/pdf')
                
        Returns:
            tuple: (success, message)
        """
        try:
            # Import mail from current app context
            mail = current_app.extensions['mail']
            
            # Normalize recipient to list
            recipients = [to] if isinstance(to, str) else to
            
            msg = Message(
                subject=subject,
                recipients=recipients,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 
                       current_app.config.get('MAIL_USERNAME'))
            )
            
            # Prepare context with standard variables
            if context is None:
                context = {}
                
            # Add standard context variables
            context.update({
                'now': datetime.now(),
                'company_name': current_app.config.get('COMPANY_NAME', 'noted;'),
                'support_email': current_app.config.get('SUPPORT_EMAIL', 'support@noted.pt'),
                'site_url': current_app.config.get('SITE_URL', 'https://noted.pt'),
                'company_address': current_app.config.get('COMPANY_ADDRESS', 'Rua da Inovação, 123<br>1000-001 Lisboa, Portugal')
            })
            
            # Render HTML template
            msg.html = render_template(template, **context)
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    try:
                        with open(attachment['path'], 'rb') as f:
                            msg.attach(
                                filename=attachment['filename'],
                                content_type=attachment.get('content_type', 'application/pdf'),
                                data=f.read()
                            )
                    except Exception as e:
                        logging.error(f"Failed to attach file {attachment['path']}: {str(e)}")
                        return False, f"Failed to attach file: {str(e)}"
            
            # Send email
            mail.send(msg)
            
            recipients_str = ', '.join(recipients)
            logging.info(f"Email sent successfully to {recipients_str} with subject: {subject}")
            return True, "Email sent successfully"
            
        except Exception as e:
            recipients_str = ', '.join(recipients) if recipients else "unknown"
            error_msg = f"Failed to send email: {str(e)}"
            logging.error(f"Failed to send email to {recipients_str}: {str(e)}")
            return False, error_msg

    @staticmethod
    def record_email_notification(order_id, notification_type, recipient_email, subject, attachments=None):
        """
        Record an email notification in the database
        
        Args:
            order_id (int): Order ID
            notification_type (str): Type of notification (e.g., 'order_confirmation')
            recipient_email (str): Recipient's email
            subject (str): Email subject
            attachments (str, optional): JSON string of attachments info
            
        Returns:
            bool: True if recorded successfully, False otherwise
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Check if email_notifications table exists, if not create it
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    notification_type VARCHAR(50) NOT NULL,
                    recipient_email VARCHAR(255) NOT NULL,
                    subject VARCHAR(255),
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'sent',
                    attachments TEXT,
                    INDEX idx_order_id (order_id),
                    INDEX idx_notification_type (notification_type)
                )
            ''')
            
            # Insert notification record
            cursor.execute('''
                INSERT INTO email_notifications 
                (order_id, notification_type, recipient_email, subject, sent_at, status, attachments)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
            ''', (order_id, notification_type, recipient_email, subject, 'sent', attachments))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Exception as e:
            logging.error(f"Failed to record email notification: {str(e)}")
            return False

    @staticmethod
    def send_registration_email(user_email, user_name, verification_token=None):
        """
        Send email verification for new user registration
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            verification_token (str): Verification token (optional, will generate if not provided)
            
        Returns:
            bool: True if email sent successfully
        """
        if not verification_token:
            from itsdangerous import URLSafeTimedSerializer
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            verification_token = serializer.dumps(
                {'email': user_email, 'timestamp': datetime.now().timestamp()},
                salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'email-salt')
            )
        
        # Generate verification URL
        verify_url = url_for('auth.verify_email', token=verification_token, _external=True)
        
        context = {
            'user_name': user_name,
            'verify_url': verify_url,
            'verification_token': verification_token
        }
        
        success, message = EmailService.send_email(
            to=user_email,
            subject="Welcome to noted; - Please verify your account",
            template='emails/registration.html',
            context=context
        )
        
        if not success:
            logging.error(f"Failed to send registration email: {message}")
            
        return success

    @staticmethod
    def send_password_reset_email(user_email, user_name, reset_token=None):
        """
        Send password reset email
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            reset_token (str): Reset token (optional, will generate if not provided)
            
        Returns:
            bool: True if email sent successfully
        """
        if not reset_token:
            from itsdangerous import URLSafeTimedSerializer
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            reset_token = serializer.dumps(
                {'email': user_email, 'timestamp': datetime.now().timestamp()},
                salt='password-reset'
            )
        
        # Generate reset URL
        reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
        
        context = {
            'user_name': user_name,
            'reset_url': reset_url,
            'reset_token': reset_token,
            'expires_in_hours': 24
        }
        
        success, message = EmailService.send_email(
            to=user_email,
            subject="Reset your noted; password",
            template='emails/password_reset.html',
            context=context
        )
        
        return success

    @staticmethod
    def send_invoice_email(user_email, user_name, order_id, invoice_number, invoice_path):
        """
        Send invoice email with PDF attachment
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            order_id (int): Order ID
            invoice_number (str): Invoice number 
            invoice_path (str): Path to the invoice PDF file
            
        Returns:
            tuple: (success, message)
        """
        from flask import current_app
        
        subject = f"Your Invoice #{invoice_number} - noted;"
        template = "emails/invoices/invoice_email.html"
        recipients = [user_email]
        context = {
            'customer_name': user_name,
            'order_id': order_id,
            'invoice_number': invoice_number,
            'app_name': "noted;"
        }
        
        try:
            # Create full path from relative path
            pdf_path = invoice_path
            if invoice_path.startswith('/static/'):
                pdf_path = os.path.join(current_app.static_folder, invoice_path.replace('/static/', ''))
                
            attachments = [(pdf_path, f'noted_invoice_{invoice_number}.pdf')]
            
            success, message = EmailService.send_email(
                to=user_email,
                subject=subject,
                template=template,
                context=context,
                attachments=[{
                    'path': pdf_path,
                    'filename': f'noted_invoice_{invoice_number}.pdf',
                    'content_type': 'application/pdf'
                }]
            )
            
            # Record the notification in the database
            if success:
                EmailService.record_email_notification(
                    order_id,
                    'invoice',
                    user_email,
                    subject,
                    invoice_path  # Store the attachment path
                )
                
            return success, message
        except Exception as e:
            logging.error(f"Failed to send invoice email: {str(e)}")
            return False, f"Failed to send invoice email: {str(e)}"

    @staticmethod
    def send_order_status_email(user_email, user_name, order):
        """
        Send order status update email
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            order: Order object containing order details
            
        Returns:
            bool: True if email sent successfully
        """
        # Set email subject based on order status
        status_map = {
            'pending': 'Order Received',
            'processing': 'Order Processing',
            'shipped': 'Order Shipped',
            'delivered': 'Order Delivered',
            'cancelled': 'Order Cancelled'
        }
        
        status_display = status_map.get(order.status, 'Order Update')
        subject = f"{status_display} #{order.id} - noted;"
        
        # Set template name
        template = 'emails/order_status.html'
        
        # Get order items and calculate totals without tax
        subtotal = sum(Decimal(str(item.unit_price)) * Decimal(str(item.quantity)) for item in order.items)
        shipping_cost = Decimal('5.0') if order.shipping_method != 'free' else Decimal('0.0')
        total = subtotal + shipping_cost
        
        success, _ = EmailService.send_email(
            to=user_email,
            subject=subject,
            template=template,
            user_name=user_name,
            order=order,
            order_status=status_display.lower(),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            app_name="noted;",
            order_date=order.order_date.strftime("%B %d, %Y")
        )
        
        # Record the notification in the database
        if success:
            notification_type = f"order_{order.status}"
            EmailService.record_email_notification(
                order.id, 
                notification_type, 
                user_email, 
                subject
            )
            
        return success

    @staticmethod
    def get_related_products(order_id, limit=4):
        """
        Get products related to the items in an order
        
        Args:
            order_id: ID of the order
            limit: Maximum number of products to return
            
        Returns:
            list: List of related product dictionaries
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # First get the product categories from the order
            cursor.execute('''
                SELECT DISTINCT p.category_id
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s AND p.category_id IS NOT NULL
            ''', (order_id,))
            
            categories = [row['category_id'] for row in cursor.fetchall()]
            
            if not categories:
                cursor.close()
                connection.close()
                return []
                
            # Get the products that were ordered (to exclude them)
            cursor.execute('''
                SELECT product_id
                FROM order_items
                WHERE order_id = %s
            ''', (order_id,))
            
            ordered_products = [row['product_id'] for row in cursor.fetchall()]
            
            # Get related products from the same categories
            # but exclude products that were already purchased
            placeholders = ', '.join(['%s'] * len(categories))
            ordered_placeholders = ', '.join(['%s'] * len(ordered_products)) if ordered_products else '0'
            
            query = f'''
                SELECT 
                    p.id, 
                    p.name, 
                    p.price, 
                    p.image,
                    CONCAT('/static/img/products/', p.image) AS image_url,
                    p.description
                FROM 
                    products p
                WHERE 
                    p.category_id IN ({placeholders})
                    AND p.id NOT IN ({ordered_placeholders})
                ORDER BY 
                    RAND()
                LIMIT %s
            '''
            
            params = categories + ordered_products + [limit]
            cursor.execute(query, params)
            
            related_products = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return related_products
            
        except Exception as e:
            logging.error(f"Error fetching related products: {str(e)}")
            return []

    @staticmethod
    def send_order_email(user_email, user_name, order, email_type='confirmation', include_invoice=True):
        """
        Universal order email method - handles confirmation, status updates, etc.
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            order: Order object containing order details
            email_type (str): Type of email ('confirmation', 'status_update')
            include_invoice (bool): Whether to attach invoice (for confirmation emails)
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Get order items with product details
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            try:
                cursor.execute('''
                    SELECT 
                        oi.*,
                        p.name AS product_name,
                        p.price AS product_price,
                        p.image AS product_image,
                        p.description AS product_description
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                ''', (order.id,))
                
                items = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching order items: {e}")
                items = []  # Default to empty list on error
            finally:
                cursor.close()
                connection.close()
            
            # Convert items to dictionaries if they are tuples
            if items and not isinstance(items[0], dict):
                columns = [col[0] for col in cursor.description]
                items = [dict(zip(columns, item)) for item in items]
                
            # Calculate order totals without tax, safely handling any data issues
            subtotal = Decimal('0')
            if items:
                try:
                    subtotal = sum(
                        Decimal(str(item.get('unit_price', 0))) * Decimal(str(item.get('quantity', 1))) 
                        for item in items
                    )
                except Exception as e:
                    print(f"Error calculating subtotal: {e}")
                    # Default to 0 if there's an error
                    subtotal = Decimal('0')
                    
            shipping_cost = Decimal('5.0') if getattr(order, 'shipping_method', '') != 'free' else Decimal('0.0')
            total = subtotal + shipping_cost
            
            # Get related products to display in email
            related_products = EmailService.get_related_products(order.id, limit=4)
            
            # Determine email subject and template based on type
            if email_type == 'confirmation':
                subject = f"Thank you for your order #{order.id} - noted;"
                template = 'emails/order_confirmation_with_invoice.html' if include_invoice else 'emails/order_confirmation.html'
            else:  # status_update
                status_map = {
                    'pending': 'Your order has been received',
                    'processing': 'Your order is being processed',
                    'shipped': 'Your order has been shipped',
                    'delivered': 'Your order has been delivered',
                    'cancelled': 'Your order has been cancelled'
                }
                subject = f"{status_map.get(order.status, 'Order status update')} - noted;"
                template = 'emails/order_status.html'
            
            # Prepare attachments and invoice link
            attachments = None
            invoice_link = None
            
            if email_type == 'confirmation' and include_invoice:
                from .invoice_service import InvoiceService
                from itsdangerous import URLSafeTimedSerializer
                
                # Generate invoice
                try:
                    invoice_service = InvoiceService()
                    result = invoice_service.generate_invoice_pdf(order.id)
                    
                    # Check if result is a tuple (which means there was an error)
                    if isinstance(result, tuple):
                        invoice_path, error = result
                        if error:
                            logging.warning(f"Could not generate invoice for order #{order.id}: {error}")
                            invoice_path = None
                    else:
                        # If it's not a tuple, assume it's just the path
                        invoice_path = result
                        error = None
                    
                    if invoice_path and isinstance(invoice_path, (str, bytes)) and not error:
                        attachments = [{
                            'path': invoice_path,
                            'filename': f'invoice_{order.id}.pdf',
                            'content_type': 'application/pdf'
                        }]
                    else:
                        logging.warning(f"No valid invoice path for order #{order.id}")
                except Exception as e:
                    logging.error(f"Error generating invoice: {e}")
                    invoice_path = None
                    
                    # Generate secure token for invoice access
                    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                    token = serializer.dumps(order.id, salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'email-salt'))
                    
                    # Generate invoice link
                    invoice_link = url_for('orders.view_invoice_secure', order_id=order.id, token=token, _external=True)
            
            # Prepare context for email template
            # Set default status for order confirmation emails
            default_status = 'processing' if email_type == 'confirmation' else 'unknown'
            order_status = getattr(order, 'status', default_status)
            
            # Ensure related_products is always a list
            if related_products is None:
                related_products = []
            
            context = {
                'user': {'name': user_name, 'email': user_email},
                'order': order,
                'items': items,
                'order_date': order.order_date.strftime("%B %d, %Y"),
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'total': total,
                'order_status': order_status,
                'invoice_link': invoice_link,
                'related_products': related_products,
                'tracking_info': {
                    'number': getattr(order, 'tracking_number', None),
                    'carrier': getattr(order, 'shipping_carrier', None),
                    'url': getattr(order, 'tracking_url', None)
                } if hasattr(order, 'tracking_number') and getattr(order, 'tracking_number', None) else None
            }
            
            # Send email
            success, message = EmailService.send_email(
                to=user_email,
                subject=subject,
                template=template,
                context=context,
                attachments=attachments
            )
            
            # Record notification
            if success:
                EmailService.record_email_notification(
                    order.id,
                    email_type,
                    user_email,
                    subject,
                    json.dumps(attachments) if attachments else None
                )
                
            return success
            
        except Exception as e:
            logging.error(f"Error sending order email: {str(e)}")
            logging.error(f"Traceback (most recent call last):\n{traceback.format_exc()}")
            return False
