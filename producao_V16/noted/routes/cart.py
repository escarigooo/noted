from flask import Blueprint, request, session, jsonify
from ..models import db, Product, Cart, Discount
import uuid

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if 'user_id' in session:
        user_id = session['user_id']
        existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            existing.quantity += quantity
        else:
            db.session.add(Cart(user_id=user_id, product_id=product_id, quantity=quantity))
        db.session.commit()
    else:
        cart = session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        session['cart'] = cart

    return jsonify({'success': True, 'message': 'Added to cart'})


@cart_bp.route('/apply_discount', methods=['POST'])
def apply_discount():
    print("\n--- APPLY DISCOUNT --- ")
    print(f"SESSION BEFORE: {dict(session)}")
    code = request.json.get('code', '').strip().upper()
    discount = Discount.query.filter_by(code=code, is_active=True).first()

    if not discount:
        return jsonify({'success': False, 'error': 'Invalid or inactive discount code'})

    # Create a unique session key for each user
    # For logged-in users, use user_id
    # For anonymous users, create a temporary user key if not exists
    if 'user_id' in session:
        user_key = f"user_{session['user_id']}"
    else:
        if 'temp_user_id' not in session:
            session['temp_user_id'] = str(uuid.uuid4())
        user_key = f"anon_{session['temp_user_id']}"
    
    print(f"GENERATED USER KEY: {user_key}")
    # Store discount with user-specific session key
    session[f'discount_{user_key}'] = {
        'code': code,
        'amount': float(discount.amount),
        'is_percentage': discount.is_percentage
    }
    
    # Make sure session is saved
    session.modified = True
    print(f"SESSION AFTER: {dict(session)}")
    
    return jsonify({
        'success': True, 
        'amount': float(discount.amount),
        'is_percentage': discount.is_percentage
    })


@cart_bp.route('/remove_discount', methods=['POST'])
def remove_discount():
    print("\n--- REMOVE DISCOUNT --- ")
    print(f"SESSION BEFORE: {dict(session)}")
    
    # Create a unique session key for each user
    if 'user_id' in session:
        user_key = f"user_{session['user_id']}"
    else:
        if 'temp_user_id' not in session:
            session['temp_user_id'] = str(uuid.uuid4())
        user_key = f"anon_{session['temp_user_id']}"
    
    print(f"USING USER KEY: {user_key}")
    
    # Remove discount from session
    discount_key = f'discount_{user_key}'
    if discount_key in session:
        del session[discount_key]
        session.modified = True
        print(f"DISCOUNT REMOVED FROM SESSION")
        print(f"SESSION AFTER: {dict(session)}")
        return jsonify({'success': True, 'message': 'Discount removed'})
    else:
        print(f"NO DISCOUNT FOUND IN SESSION")
        return jsonify({'success': False, 'error': 'No discount to remove'})


@cart_bp.route('/cart_data')
def cart_data():
    print("\n--- CART DATA ---")
    print(f"SESSION: {dict(session)}")
    items = []

    # Create a unique user key for session storage
    if 'user_id' in session:
        user_key = f"user_{session['user_id']}"
        user_id = session['user_id']
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                continue
            color = next((f.value for f in product.features if f.feature_type.name.lower() == 'color'), None)
            items.append({
                'id': product.id,
                'name': product.name,
                'color': color,
                'price': float(product.price),
                'image': product.image,
                'quantity': item.quantity
            })
    else:
        if 'temp_user_id' not in session:
            session['temp_user_id'] = str(uuid.uuid4())
        user_key = f"anon_{session['temp_user_id']}"
        cart = session.get('cart', {})
        for product_id_str, quantity in cart.items():
            product = Product.query.get(int(product_id_str))
            if not product:
                continue
            color = next((f.value for f in product.features if f.feature_type.name.lower() == 'color'), None)
            items.append({
                'id': product.id,
                'name': product.name,
                'color': color,
                'price': float(product.price),
                'image': product.image,
                'quantity': quantity
            })

    print(f"USING USER KEY: {user_key}")

    total = sum(item['price'] * item['quantity'] for item in items)
    total_after_discount = total
    discount_applied = None

    # Get discount using the user-specific key
    discount_data = session.get(f'discount_{user_key}')
    if discount_data:
        discount_code = discount_data.get('code')
        discount = Discount.query.filter_by(code=discount_code, is_active=True).first()
        if discount:
            discount_applied = {
                'code': discount.code,
                'amount': float(discount_data.get('amount')),
                'is_percentage': bool(discount_data.get('is_percentage'))
            }

            if discount_applied['is_percentage']:
                total_after_discount = total * (1 - discount_applied['amount'] / 100)
            else:
                total_after_discount = total - discount_applied['amount']

    return jsonify({
        'success': True,
        'items': items,
        'total': round(total, 2),
        'discount': discount_applied,
        'total_after_discount': round(max(total_after_discount, 0), 2)
    })


@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))

    if 'user_id' in session:
        user_id = session['user_id']
        item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify(success=True)
    else:
        cart = session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart
            return jsonify(success=True)

    return jsonify(success=False)


@cart_bp.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    delta = data.get('delta', 0)

    if 'user_id' in session:
        user_id = session['user_id']
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity = max(1, cart_item.quantity + delta)
            db.session.commit()
            return jsonify(success=True)
        return jsonify(success=False, error="Item not found")

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] = max(1, cart[product_id] + delta)
        session['cart'] = cart
        return jsonify(success=True)

    return jsonify(success=False, error="Item not found in session"), 404
