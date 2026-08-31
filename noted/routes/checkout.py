from flask import Blueprint, current_app, render_template, redirect, url_for, request, session, jsonify
from ..models import BillingAddress, Discount, NotedCashTransaction, Order, OrderItem, PaymentInfo, Product, ShippingAddress, db, User, Cart
from ..services import EmailService

from datetime import datetime
from decimal import Decimal, InvalidOperation

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route("/checkout")
def checkout():
    if 'user_id' not in session:
        return redirect(url_for("auth.login", success="please log in to continue"))

    user = db.session.get(User, session['user_id'])
    if not user:
        return redirect(url_for("auth.login"))

    session['user_email'] = user.email
    session['user_balance'] = float(user.noted_cash or 0)
    cart_items = Cart.query.filter_by(user_id=user.id).all()

    if not cart_items:
        return redirect(url_for("auth.account"))

    return render_template("pages/account/checkout.html", cart_items=cart_items)


@checkout_bp.route("/cart-total")
def cart_total():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return jsonify({"success": True, "total": float(total)})


@checkout_bp.route('/place-order', methods=['POST'])
def place_order():
    data = request.get_json(silent=True) or {}
    total_confirmed = data.get("total_confirmed", 0.0)
    
    try:
        total_confirmed = Decimal(str(total_confirmed))
    except InvalidOperation:
        return jsonify({"success": False, "message": "Invalid total format"}), 400

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not authenticated'}), 401

    try:
        shipping_data = data.get("shipping") or {}
        billing_data = data.get("billing") or {}
        shipping_method = data.get('shippingMethod')
        payment_method = data.get('paymentMethod')
        billing_same = data.get('billingSameAsShipping', True)

        required_fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'zip_code', 'country', 'phone', 'email']
        for field in required_fields:
            if not shipping_data.get(field):
                return jsonify({'success': False, 'message': f'Missing shipping field: {field}'}), 400
            if not billing_same and not billing_data.get(field):
                return jsonify({'success': False, 'message': f'Missing billing field: {field}'}), 400

        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({"success": False, "message": "Cart is empty"}), 400

        # Calculate the original subtotal - Add defensive checks
        real_total = Decimal('0.00')
        for item in cart_items:
            if item.product is None:
                continue  # Skip items with missing product references
            product_price = getattr(item.product, 'price', None)
            if product_price is not None:
                real_total += Decimal(str(product_price)) * item.quantity
        
        # Check for discount data from client
        discount_value = Decimal('0.00')
        if data.get('discount_details'):
            discount_data = data.get('discount_details')
            discount_code = discount_data.get('code')
            
            # Verify the discount exists and is valid
            discount = Discount.query.filter_by(code=discount_code).first()
            if discount and discount.is_active:
                # Apply discount
                if discount.is_percentage:
                    discount_value = real_total * (Decimal(str(discount.amount)) / Decimal('100'))
                else:
                    discount_value = Decimal(str(discount.amount))
                
                # Cap discount at the cart total
                if discount_value > real_total:
                    discount_value = real_total
        
        # Apply discount to total
        discounted_total = real_total - discount_value
        
        # Shipping prices are authoritative on the server.
        shipping_rates = {"free": Decimal("0.00"), "express": Decimal("9.90")}
        if shipping_method not in shipping_rates:
            return jsonify({"success": False, "message": "Invalid shipping method"}), 400
        shipping_cost = shipping_rates[shipping_method]
        final_total = discounted_total + shipping_cost
        
        if payment_method not in {"card", "account"}:
            return jsonify({"success": False, "message": "Invalid payment method"}), 400

        if abs(final_total - total_confirmed) > Decimal("0.01"):
            return jsonify({
                "success": False,
                "message": "Cart total changed. Please review the order and try again.",
            }), 400

        payment_total = final_total

        order = Order(
            user_id=user_id,
            order_date=datetime.now(),
            total=payment_total,  # Use the payment_total which accounts for discounts
            shipping_method=shipping_method,
            payment_method=payment_method,
            billing_same_as_shipping=billing_same
        )
        db.session.add(order)
        db.session.flush()

        shipping = ShippingAddress(order_id=order.id, **shipping_data)
        db.session.add(shipping)

        billing = BillingAddress(order_id=order.id, **(shipping_data if billing_same else billing_data))
        db.session.add(billing)

        if payment_method == "card":
            # Portfolio demo only: no card details are collected or processed.
            last4 = None
            brand = "Demo card"
        else:
            last4 = None
            brand = "Noted Cash"
            user = db.session.get(User, user_id)

            # If the order is free after discounts, skip the balance check
            # Clear logic for free order vs. insufficient balance
            if payment_total <= Decimal("0.01"):
                pass
            elif not user or Decimal(user.noted_cash or 0) < payment_total:
                return jsonify({'success': False, 'message': 'Insufficient Noted Cash balance'}), 400
            else:
                # Only deduct from user balance if there's an actual cost
                if payment_total > Decimal("0.01"):
                    user.noted_cash = Decimal(user.noted_cash or 0) - payment_total
                    db.session.add(NotedCashTransaction(
                        user_id=user_id,
                        change_amount=-payment_total,
                        reason='Order payment'
                    ))

        payment = PaymentInfo(
            order_id=order.id,
            card_last4=last4,
            card_brand=brand,
            paid=True,
            payment_date=datetime.now()
        )
        db.session.add(payment)

        # When creating order items, add defensive checks
        for item in cart_items:
            if item.product is None:
                continue  # Skip items with missing products
                
            product_price = getattr(item.product, 'price', Decimal('0.00'))
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product_price
            )
            db.session.add(order_item)

        Cart.query.filter_by(user_id=user_id).delete()

        db.session.commit()
        
        # Send order confirmation email
        user = db.session.get(User, user_id)
        if user:
            try:
                # Use the unified send_order_email method with default parameters for order confirmation
                EmailService.send_order_email(user.email, user.name, order)
            except Exception as e:
                current_app.logger.warning("Order confirmation email failed")
                # Don't fail the order if email fails
        
        return jsonify({'success': True, 'message': 'Order placed successfully'})

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Order placement failed")
        return jsonify({"success": False, "message": "Unable to place order"}), 500


@checkout_bp.route("/set_shipping", methods=["POST"])
def set_shipping():
    data = request.get_json()
    # lógica para calcular preço de envio, por exemplo
    return jsonify({"success": True, "price": 0.00})

@checkout_bp.route("/is_logged_in")
def is_logged_in():
    if "user_id" in session:
        return jsonify({"logged_in": True})
    return jsonify({"logged_in": False})


@checkout_bp.route("/thank-you")
def thank_you():
    """
    Render the thank you page after a successful order
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for("auth.login"))
    
    # Find the most recent order for this user
    order = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).first()
    
    return render_template("pages/account/thank-you.html", order=order)
