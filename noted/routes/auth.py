from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import db, User, Cart, get_db_connection
from ..security import password_error
from ..services import EmailService

auth_bp = Blueprint('auth', __name__)
PASSWORD_RESET_MAX_AGE = 24 * 60 * 60


# Serializer com current_app (funciona dentro de contexto Flask)
def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def start_user_session(user):
    """Replace the current session with the authenticated user identity."""
    session.clear()
    session.permanent = True
    session["user_id"] = user.id
    session["user_email"] = user.email
    session["user_name"] = user.name


# ---------------------- LOGIN ---------------------- #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    success = request.args.get("success")

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.email_verified and check_password_hash(user.password, password):
            # integrar carrinho de guest
            guest_cart = session.get('cart', {})
            next_page = session.get("next_after_login")
            start_user_session(user)
            for product_id_str, quantity in guest_cart.items():
                product_id = int(product_id_str)
                existing = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
                if existing:
                    existing.quantity += quantity
                else:
                    db.session.add(Cart(user_id=user.id, product_id=product_id, quantity=quantity))
            db.session.commit()

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
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("pages/auth/register.html", error="passwords do not match")

        validation_error = password_error(password)
        if validation_error:
            return render_template("pages/auth/register.html", error=validation_error)

        if User.query.filter_by(email=email).first():
            return render_template("pages/auth/register.html", error="email already registered")

        try:
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password, method="pbkdf2:sha256"),
                email_verified=False,
            )
            db.session.add(new_user)
            db.session.flush()

            token = get_serializer().dumps(
                {"user_id": new_user.id, "email": new_user.email},
                salt="email-confirm",
            )
            if EmailService.send_registration_email(email, name, token):
                db.session.commit()
                return render_template(
                    "pages/auth/register.html",
                    success="check your email to verify your account.",
                )

            db.session.rollback()
            return render_template(
                "pages/auth/register.html",
                error="failed to send verification email. please try again.",
            )
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Registration failed")
            return render_template(
                "pages/auth/register.html",
                error="An error occurred during registration. Please try again.",
            )

    return render_template("pages/auth/register.html")


# ---------------------- VERIFICACAO DO TOKEN ---------------------- #
@auth_bp.route("/verify/<token>")
def verify_email(token):
    try:
        data = get_serializer().loads(token, salt="email-confirm", max_age=3600)
        user = User.query.filter_by(
            id=data.get("user_id"),
            email=data.get("email"),
        ).first()
        if not user:
            return redirect(url_for("auth.register", error="invalid token content"))

        if user.email_verified:
            return redirect(
                url_for("auth.login", success="this email is already verified.")
            )

        user.email_verified = True
        db.session.commit()
        return redirect(
            url_for("auth.login", success="account verified! you can now log in.")
        )
    except Exception:
        current_app.logger.info("Invalid or expired email verification token")
        return redirect(
            url_for("auth.register", error="invalid or expired verification link.")
        )


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
    
    user = db.session.get(User, session['user_id'])
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


@auth_bp.route("/account/password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not check_password_hash(user.password, current_password):
            return render_template(
                "pages/account/change_password.html",
                error="current password is incorrect.",
            )
        if new_password != confirm:
            return render_template(
                "pages/account/change_password.html",
                error="passwords do not match.",
            )

        validation_error = password_error(new_password)
        if validation_error:
            return render_template(
                "pages/account/change_password.html",
                error=validation_error,
            )
        if check_password_hash(user.password, new_password):
            return render_template(
                "pages/account/change_password.html",
                error="new password must be different from the current password.",
            )

        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()
        start_user_session(user)
        return redirect(
            url_for("auth.account", success="password updated successfully.")
        )

    return render_template("pages/account/change_password.html")


# ---------------------- ESQUECI A SENHA ---------------------- #
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            token = get_serializer().dumps(
                {"user_id": user.id, "email": user.email},
                salt="reset-password",
            )
            if not EmailService.send_password_reset_email(user.email, user.name, token):
                current_app.logger.warning(
                    "Password reset email could not be sent for user %s",
                    user.id,
                )

        return render_template(
            "pages/auth/forgot_password.html",
            success="if that account exists, a reset link has been sent.",
        )

    return render_template("pages/auth/forgot_password.html")

# ---------------------- REDEFINIR SENHA ---------------------- #
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        data = get_serializer().loads(
            token,
            salt="reset-password",
            max_age=PASSWORD_RESET_MAX_AGE,
        )
    except Exception:
        current_app.logger.info("Invalid or expired password reset token")
        return render_template("pages/auth/login.html", error="invalid or expired reset link.")

    if isinstance(data, dict):
        user = User.query.filter_by(
            id=data.get("user_id"),
            email=data.get("email"),
        ).first()
    else:
        # Accept reset links created before structured tokens were introduced.
        user = User.query.filter_by(email=data).first()

    if not user:
        current_app.logger.info("Password reset token references a missing user")
        return render_template("pages/auth/login.html", error="invalid or expired reset link.")

    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if new_password != confirm:
            return render_template("pages/auth/reset_password.html", token=token, error="passwords do not match")

        validation_error = password_error(new_password)
        if validation_error:
            return render_template(
                "pages/auth/reset_password.html",
                token=token,
                error=validation_error,
            )

        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()

        # Integrate cart items if there are any in the guest session
        guest_cart = session.get('cart', {})
        start_user_session(user)
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
