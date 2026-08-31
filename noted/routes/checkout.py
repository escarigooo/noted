from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from ..models import BillingAddress, Discount, NotedCashTransaction, Order, OrderItem, PaymentInfo, Product, ShippingAddress, db, User, Cart
from ..services import EmailService

from datetime import datetime
from decimal import Decimal, InvalidOperation

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route("/checkout")
def checkout():
    if 'user_id' not in session:
        return redirect(url_for("auth.login", success="please log in to continue"))

    user = User.query.get(session['user_id'])
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
    data = request.get_json()
    total_confirmed = data.get('total_confirmed', 0.0)

    # Debug logging
    print("Received order data:", data)
    print(f"Payment method: {data.get('paymentMethod')}")
    print(f"Free order flag: {data.get('free_order', False)}")
    print(f"Requires no balance flag: {data.get('requires_no_balance', False)}")
    print(f"Actual payment required: {data.get('actual_payment_required', 'Not specified')}")
    print(f"Total confirmed: {total_confirmed}")
    
    try:
        total_confirmed = Decimal(str(total_confirmed))
    except InvalidOperation:
        return jsonify({"success": False, "message": "Invalid total format"}), 400

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not authenticated'}), 401

    try:
        shipping_data = data.get('shipping')
        billing_data = data.get('billing')
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
        
        # Add shipping cost
        shipping_cost = Decimal(str(data.get('shipping_cost', 0.0)))
        final_total = discounted_total + shipping_cost
        
        # Handle free order case with proper validation
        free_order = data.get('free_order', False)
        requires_no_balance = data.get('requires_no_balance', False)
        actual_payment_required = Decimal(str(data.get('actual_payment_required', final_total)))
        
        # For free orders, we still validate the original total was sent correctly
        # but we'll process the order with zero cost
        if free_order and requires_no_balance and final_total <= Decimal('0.01'):
            # This is a legitimate free order
            payment_total = Decimal('0.00')
            print("Processing as FREE ORDER with zero payment")
        else:
            # Regular order with payment required
            payment_total = final_total
            print(f"Processing as REGULAR ORDER with payment: {payment_total}")
            
            # Still verify the client knows the correct original total
            if abs(real_total - total_confirmed) > Decimal("0.01"):
                return jsonify({
                    "success": False,
                    "message": f"Cart total mismatch: {real_total:.2f}€ vs {total_confirmed:.2f}€"
                }), 400

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

        if payment_method == 'card':
            card_number = data['payment'].get('card_number', '')
            last4 = card_number[-4:] if card_number else None
            brand = "Unknown"
        else:
            last4 = None
            brand = "Noted Cash"
            user = User.query.get(user_id)

            # Check if this is a free order (zero cost after discounts)
            # free_order already defined above, no need to redefine
            print(f"Free order check - free_order: {free_order}, requires_no_balance: {requires_no_balance}")
            print(f"Final total: {final_total}, Payment total: {payment_total}")
            
            if user:
                print(f"User noted_cash balance: {user.noted_cash}")
            else:
                print("User not found")
            
            # If the order is free after discounts, skip the balance check
            # Clear logic for free order vs. insufficient balance
            if payment_total <= Decimal("0.01"):
                # Zero payment order, allow regardless of balance
                print("Zero payment order - allowing without balance check")
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
                else:
                    print("Zero payment order - no Noted Cash transaction needed")

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
        user = User.query.get(user_id)
        if user:
            try:
                # Use the unified send_order_email method with default parameters for order confirmation
                EmailService.send_order_email(user.email, user.name, order)
            except Exception as e:
                print(f"Failed to send order confirmation email: {e}")
                # Don't fail the order if email fails
        
        return jsonify({'success': True, 'message': 'Order placed successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


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