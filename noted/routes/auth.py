from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import current_app  # necessário para usar o get_serializer
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from ..models import db, User, Cart, get_db_connection
from ..services import EmailService

auth_bp = Blueprint('auth', __name__)

# Serializer com current_app (funciona dentro de contexto Flask)
def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

# ---------------------- LOGIN ---------------------- #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    success = request.args.get("success")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name

            # integrar carrinho de guest
            guest_cart = session.pop('cart', {})
            for product_id_str, quantity in guest_cart.items():
                product_id = int(product_id_str)
                existing = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
                if existing:
                    existing.quantity += quantity
                else:
                    db.session.add(Cart(user_id=user.id, product_id=product_id, quantity=quantity))
            db.session.commit()

            next_page = session.pop("next_after_login", None)
            if user.role == 1:
                return redirect(url_for("admin.dashboard"))
            elif next_page:
                return redirect(url_for(next_page))
            return redirect(url_for("auth.account"))

        return render_template("pages/auth/login.html", error="invalid email or password", success=success)

    return render_template("pages/auth/login.html", success=success)

# ---------------------- REGISTO ---------------------- #
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("pages/auth/register.html", error="passwords do not match")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("pages/auth/register.html", error="email already registered")

        try:
            token_data = {"name": name, "email": email, "password": password}
            token = get_serializer().dumps(token_data, salt="email-confirm")

            verify_link = url_for("auth.verify_email", token=token, _external=True)
            print(f"[DEBUG] Email verification link: {verify_link}")

            # Send verification email
            email_sent = EmailService.send_registration_email(email, name, token)
            
            if email_sent:
                return render_template("pages/auth/register.html", success="check your email to verify your account.")
            else:
                # Debugging information
                print("[ERROR] Failed to send registration email")
                from flask import current_app
                print(f"[DEBUG] Email Config: {current_app.config.get('MAIL_SERVER')}, "
                      f"Port: {current_app.config.get('MAIL_PORT')}, "
                      f"Username: {current_app.config.get('MAIL_USERNAME')}")
                return render_template("pages/auth/register.html", error="failed to send verification email. please try again.")
        except Exception as e:
            print(f"[ERROR] Registration exception: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return render_template("pages/auth/register.html", error="An error occurred during registration. Please try again.")

    return render_template("pages/auth/register.html")

# ---------------------- VERIFICAÇÃO DO TOKEN ---------------------- #
@auth_bp.route("/verify/<token>")
def verify_email(token):
    try:
        print("[DEBUG] Token recebido:", token)

        data = get_serializer().loads(token, salt="email-confirm", max_age=3600)
        print("[DEBUG] Dados do token:", data)

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not all([name, email, password]):
            return redirect(url_for("auth.register", error="invalid token content"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for("auth.login", success="this email is already verified."))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login", success="account verified! you can now log in."))

    except Exception as e:
        print(f"[DEBUG] verification error: {e}")
        return redirect(url_for("auth.register", error="invalid or expired verification link."))

# ---------------------- LOGOUT ---------------------- #
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_email", None)
    session.pop("user_name", None)
    return redirect(url_for("misc.index"))

# ---------------------- CONTA ---------------------- #
@auth_bp.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for("auth.login"))
    
    # Get success message if passed
    success = request.args.get("success")
    
    # Get user's orders with all details
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get orders with basic information
    cursor.execute('''
        SELECT 
            o.*,
            COUNT(oi.id) AS item_count,
            (SELECT SUM(oi2.quantity) FROM order_items oi2 WHERE oi2.order_id = o.id) AS total_items
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = %s
        GROUP BY o.id
        ORDER BY o.order_date DESC
    ''', (user.id,))
    
    orders = cursor.fetchall()
    
    # Get invoices for the user
    cursor.execute('''
        SELECT 
            i.*,
            o.id AS order_id,
            o.total AS order_total,
            o.status AS order_status,
            o.order_date AS order_date
        FROM invoices i
        JOIN orders o ON i.order_id = o.id
        WHERE o.user_id = %s
        ORDER BY i.invoice_date DESC
    ''', (user.id,))
    
    invoices = cursor.fetchall()
    
    # Get noted cash transactions
    cursor.execute('''
        SELECT * FROM noted_cash_transactions
        WHERE user_id = %s
        ORDER BY created_at DESC
    ''', (user.id,))
    
    cash_transactions = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Format dates
    for order in orders:
        if order['order_date']:
            order['formatted_date'] = order['order_date'].strftime('%d %b, %Y')
    
    for invoice in invoices:
        if invoice['invoice_date']:
            invoice['formatted_date'] = invoice['invoice_date'].strftime('%d %b, %Y')
        if invoice['order_date']:
            invoice['formatted_order_date'] = invoice['order_date'].strftime('%d %b, %Y')
    
    for transaction in cash_transactions:
        if transaction['created_at']:
            transaction['formatted_date'] = transaction['created_at'].strftime('%d %b, %Y')
    
    # Add joined date if not present
    if hasattr(user, 'created_at'):
        user.joined_date = user.created_at.strftime('%d %b, %Y')
    else:
        user.joined_date = "N/A"
    
    return render_template(
        "pages/account/account.html", 
        user=user, 
        orders=orders, 
        invoices=invoices, 
        cash_transactions=cash_transactions,
        success=success
    )

# ---------------------- ESQUECI A SENHA ---------------------- #
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()

        if user:
            token = get_serializer().dumps(user.email, salt="reset-password")
            reset_link = url_for("auth.reset_password", token=token, _external=True)
            print(f"[debug] password reset link: {reset_link}")
            
            # Send password reset email
            email_sent = EmailService.send_password_reset_email(user.email, user.name, token)
            
            if email_sent:
                return render_template("pages/auth/forgot_password.html", success="check your email for the reset link.")
            else:
                return render_template("pages/auth/forgot_password.html", error="failed to send reset email. please try again.")
        else:
            return render_template("pages/auth/forgot_password.html", error="email not found.")

    return render_template("pages/auth/forgot_password.html")

# ---------------------- REDEFINIR SENHA ---------------------- #
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = get_serializer().loads(token, salt="reset-password", max_age=3600)
    except Exception as e:
        print(f"[debug] invalid or expired reset link: {e}")
        return render_template("pages/auth/login.html", error="invalid or expired reset link.")

    if request.method == "POST":
        new_password = request.form["password"]
        confirm = request.form["confirm"]
        if new_password != confirm:
            return render_template("pages/auth/reset_password.html", token=token, error="passwords do not match")

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()
        
        # Automatically log in the user after password reset
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.name
        
        # Integrate cart items if there are any in the guest session
        guest_cart = session.pop('cart', {})
        for product_id_str, quantity in guest_cart.items():
            product_id = int(product_id_str)
            existing = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
            if existing:
                existing.quantity += quantity
            else:
                db.session.add(Cart(user_id=user.id, product_id=product_id, quantity=quantity))
        db.session.commit()
        
        # Redirect to account page or homepage
        if user.role == 1:
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("auth.account", success="password updated successfully. you've been automatically logged in."))

    return render_template("pages/auth/reset_password.html", token=token)
