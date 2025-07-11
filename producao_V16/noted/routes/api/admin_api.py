from flask import Blueprint, jsonify, request
from noted.models import User, Product, Category, Order
import mysql.connector
from datetime import datetime
from functools import wraps
import hashlib

# Create Blueprint
admin_api = Blueprint('admin_api', __name__)

# Database connection helper
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_noted'
        )
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise

# Admin authentication for API endpoints
def admin_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session
        from noted.models import User
        
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
            
        user = User.query.get(user_id)
        if not user or user.role != 1:  # 1 = admin
            return jsonify({"error": "Admin privileges required"}), 403
            
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# CATEGORIES API ENDPOINTS
# ============================================================================

@admin_api.route('/api/admin/table/categories', methods=['GET'])
@admin_required_api
def get_categories_table():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 25))
        search = request.args.get('search', '')
        filter_value = request.args.get('filter', 'all')
        sort_column = request.args.get('sort_column', 'id')
        sort_direction = request.args.get('sort_direction', 'asc')
        
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("categories.description LIKE %s")
            params.append(f'%{search}%')
        
        if filter_value == 'with_products':
            where_conditions.append("product_count > 0")
        elif filter_value == 'without_products':
            where_conditions.append("product_count = 0")
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)

        # Get total count
        count_query = f'''
            SELECT COUNT(*) as total
            FROM (
                SELECT categories.id
                FROM categories
                LEFT JOIN (
                    SELECT category_id, COUNT(*) as product_count
                    FROM products
                    GROUP BY category_id
                ) pc ON categories.id = pc.category_id
                {where_clause}
            ) as filtered_categories
        '''
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']

        # Main query
        valid_columns = ['id', 'description', 'product_count']
        if sort_column not in valid_columns:
            sort_column = 'id'
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'asc'

        query = f'''
            SELECT 
                categories.id,
                categories.description,
                COALESCE(pc.product_count, 0) as product_count
            FROM categories
            LEFT JOIN (
                SELECT category_id, COUNT(*) as product_count
                FROM products
                GROUP BY category_id
            ) pc ON categories.id = pc.category_id
            {where_clause}
            ORDER BY {sort_column} {sort_direction}
            LIMIT %s OFFSET %s
        '''
        
        cursor.execute(query, params + [per_page, offset])
        categories = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "data": categories,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }), 200

    except Exception as e:
        print(f"Error fetching categories: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch categories"}), 500

@admin_api.route('/api/admin/table/categories', methods=['POST'])
@admin_required_api
def create_category():
    try:
        data = request.get_json()
        description = data.get('description')
        
        if not description:
            return jsonify({"success": False, "message": "Description is required"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "INSERT INTO categories (description) VALUES (%s)",
            (description,)
        )
        
        category_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": "Category created successfully",
            "id": category_id
        }), 201

    except Exception as e:
        print(f"Error creating category: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create category"}), 500

@admin_api.route('/api/admin/categories/<int:category_id>', methods=['GET'])
@admin_required_api
def get_category_details(category_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        
        if not category:
            return jsonify({"success": False, "message": "Category not found"}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "data": category}), 200

    except Exception as e:
        print(f"Error fetching category: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch category"}), 500

@admin_api.route('/api/admin/categories/<int:category_id>', methods=['PUT'])
@admin_required_api
def update_category(category_id):
    try:
        data = request.get_json()
        description = data.get('description')
        
        if not description:
            return jsonify({"success": False, "message": "Description is required"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "UPDATE categories SET description = %s WHERE id = %s",
            (description, category_id)
        )
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Category not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Category updated successfully"}), 200

    except Exception as e:
        print(f"Error updating category: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update category"}), 500

@admin_api.route('/api/admin/table/categories/<int:category_id>', methods=['DELETE'])
@admin_required_api
def delete_category_table(category_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if category has products
        cursor.execute("SELECT COUNT(*) as count FROM products WHERE category_id = %s", (category_id,))
        product_count = cursor.fetchone()[0]
        
        if product_count > 0:
            return jsonify({
                "success": False, 
                "message": f"Cannot delete category with {product_count} products. Move products first."
            }), 400
        
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Category not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Category deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting category: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete category"}), 500

# ============================================================================
# PRODUCTS API ENDPOINTS
# ============================================================================

@admin_api.route('/api/admin/table/products', methods=['GET'])
@admin_required_api
def get_products_table():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 25))
        search = request.args.get('search', '')
        filter_value = request.args.get('filter', 'all')
        sort_column = request.args.get('sort_column', 'id')
        sort_direction = request.args.get('sort_direction', 'asc')
        include_stock = request.args.get('include_stock', 'true').lower() == 'true'
        
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(products.name LIKE %s OR categories.description LIKE %s)")
            params.extend([f'%{search}%', f'%{search}%'])
        
        if filter_value and filter_value != 'all':
            if filter_value.isdigit():
                where_conditions.append("products.category_id = %s")
                params.append(int(filter_value))
            elif filter_value == 'out_of_stock':
                where_conditions.append("(product_stock.quantity = 0 OR product_stock.quantity IS NULL)")
            elif filter_value == 'low_stock':
                where_conditions.append("product_stock.quantity <= 10 AND product_stock.quantity > 0")
            elif filter_value == 'in_stock':
                where_conditions.append("product_stock.quantity > 10")
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)

        # Get total count
        count_query = f'''
            SELECT COUNT(*) as total
            FROM products
            LEFT JOIN categories ON products.category_id = categories.id
            LEFT JOIN product_stock ON products.id = product_stock.product_id
            {where_clause}
        '''
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']

        # Main query
        valid_columns = ['id', 'name', 'price', 'category_description', 'created_at', 'stock_quantity']
        if sort_column not in valid_columns:
            sort_column = 'id'
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'asc'

        query = f'''
            SELECT 
                products.id,
                products.name,
                products.price,
                products.description,
                products.image,
                products.created_at,
                categories.description as category_description,
                products.category_id,
                COALESCE(product_stock.quantity, 0) as stock_quantity
            FROM products
            LEFT JOIN categories ON products.category_id = categories.id
            LEFT JOIN product_stock ON products.id = product_stock.product_id
            {where_clause}
            ORDER BY {sort_column} {sort_direction}
            LIMIT %s OFFSET %s
        '''
        
        cursor.execute(query, params + [per_page, offset])
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "data": products,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }), 200

    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch products"}), 500

@admin_api.route('/api/admin/table/products', methods=['POST'])
@admin_required_api
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        category_id = data.get('category_id')
        description = data.get('description', '')
        image = data.get('image', '')
        initial_stock = data.get('initial_stock', 0)  # Allow setting initial stock
        
        if not name or not price or not category_id:
            return jsonify({"success": False, "message": "Name, price, and category are required"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert product
        cursor.execute('''
            INSERT INTO products (name, price, category_id, description, image, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, price, category_id, description, image, datetime.now()))
        
        product_id = cursor.lastrowid
        
        # Create initial stock record
        cursor.execute('''
            INSERT INTO product_stock (product_id, quantity)
            VALUES (%s, %s)
        ''', (product_id, initial_stock))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": "Product created successfully",
            "id": product_id
        }), 201

    except Exception as e:
        print(f"Error creating product: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create product"}), 500

@admin_api.route('/api/admin/products/<int:product_id>', methods=['GET'])
@admin_required_api
def get_product_details(product_id):
    try:
        include_stock = request.args.get('include_stock', 'false').lower() == 'true'
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if include_stock:
            cursor.execute('''
                SELECT 
                    products.*, 
                    categories.description as category_description,
                    COALESCE(product_stock.quantity, 0) as stock_quantity
                FROM products
                LEFT JOIN categories ON products.category_id = categories.id
                LEFT JOIN product_stock ON products.id = product_stock.product_id
                WHERE products.id = %s
            ''', (product_id,))
        else:
            cursor.execute('''
                SELECT products.*, categories.description as category_description
                FROM products
                LEFT JOIN categories ON products.category_id = categories.id
                WHERE products.id = %s
            ''', (product_id,))
        
        product = cursor.fetchone()
        
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "data": product}), 200

    except Exception as e:
        print(f"Error fetching product: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch product"}), 500

@admin_api.route('/api/admin/products/<int:product_id>', methods=['PUT'])
@admin_required_api
def update_product(product_id):
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            params.append(data['name'])
        if 'price' in data:
            update_fields.append("price = %s")
            params.append(data['price'])
        if 'category_id' in data:
            update_fields.append("category_id = %s")
            params.append(data['category_id'])
        if 'description' in data:
            update_fields.append("description = %s")
            params.append(data['description'])
        if 'image' in data:
            update_fields.append("image = %s")
            params.append(data['image'])
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        params.append(product_id)
        
        cursor.execute(f'''
            UPDATE products SET {', '.join(update_fields)}
            WHERE id = %s
        ''', params)
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Product updated successfully"}), 200

    except Exception as e:
        print(f"Error updating product: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update product"}), 500

@admin_api.route('/api/admin/table/products/<int:product_id>', methods=['DELETE'])
@admin_required_api
def delete_product_table(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if product is in any orders
        cursor.execute("SELECT COUNT(*) as count FROM order_items WHERE product_id = %s", (product_id,))
        order_count = cursor.fetchone()[0]
        
        if order_count > 0:
            return jsonify({
                "success": False, 
                "message": f"Cannot delete product that appears in {order_count} orders."
            }), 400
        
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Product deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting product: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete product"}), 500

# ============================================================================
# USERS API ENDPOINTS
# ============================================================================

@admin_api.route('/api/admin/table/users', methods=['GET'])
@admin_required_api
def get_users_table():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 25))
        search = request.args.get('search', '')
        filter_value = request.args.get('filter', 'all')
        sort_column = request.args.get('sort_column', 'id')
        sort_direction = request.args.get('sort_direction', 'asc')
        
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(users.name LIKE %s OR users.email LIKE %s)")
            params.extend([f'%{search}%', f'%{search}%'])
        
        if filter_value == 'admin':
            where_conditions.append("users.role = 1")
        elif filter_value == 'customer':
            where_conditions.append("users.role = 2")
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)

        # Get total count
        count_query = f'''
            SELECT COUNT(*) as total
            FROM users
            {where_clause}
        '''
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']

        # Main query
        valid_columns = ['id', 'name', 'email', 'role', 'noted_cash', 'created_at']
        if sort_column not in valid_columns:
            sort_column = 'id'
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'asc'

        query = f'''
            SELECT 
                users.id,
                users.name,
                users.email,
                users.role,
                users.noted_cash,
                users.address,
                users.created_at,
                COUNT(DISTINCT orders.id) as order_count
            FROM users
            LEFT JOIN orders ON users.id = orders.user_id
            {where_clause}
            GROUP BY users.id
            ORDER BY {sort_column} {sort_direction}
            LIMIT %s OFFSET %s
        '''
        
        cursor.execute(query, params + [per_page, offset])
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "data": users,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }), 200

    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch users"}), 500

@admin_api.route('/api/admin/table/users', methods=['POST'])
@admin_required_api
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 2)  # Default to customer
        address = data.get('address', '')
        noted_cash = data.get('noted_cash', 0.0)
        
        if not name or not email or not password:
            return jsonify({"success": False, "message": "Name, email, and password are required"}), 400
        
        # Hash password (using simple hash for testing - replace with proper bcrypt in production)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Email already exists"}), 400
        
        cursor.execute('''
            INSERT INTO users (name, email, password, role, address, noted_cash, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, email, hashed_password, role, address, noted_cash, datetime.now()))
        
        user_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "id": user_id
        }), 201

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create user"}), 500

@admin_api.route('/api/admin/users/<int:user_id>', methods=['GET'])
@admin_required_api
def get_user_details(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT 
                users.*,
                COUNT(DISTINCT orders.id) as order_count,
                SUM(orders.total) as total_spent
            FROM users
            LEFT JOIN orders ON users.id = orders.user_id
            WHERE users.id = %s
            GROUP BY users.id
        ''', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Don't return password
        user.pop('password', None)
        
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "data": user}), 200

    except Exception as e:
        print(f"Error fetching user: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch user"}), 500

@admin_api.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@admin_required_api
def update_user(user_id):
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            params.append(data['name'])
        if 'email' in data:
            # Check if new email is already taken by another user
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = %s AND id != %s", 
                         (data['email'], user_id))
            if cursor.fetchone()[0] > 0:
                return jsonify({"success": False, "message": "Email already exists"}), 400
            update_fields.append("email = %s")
            params.append(data['email'])
        if 'password' in data and data['password']:
            hashed_password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
            update_fields.append("password = %s")
            params.append(hashed_password)
        if 'role' in data:
            update_fields.append("role = %s")
            params.append(data['role'])
        if 'address' in data:
            update_fields.append("address = %s")
            params.append(data['address'])
        if 'noted_cash' in data:
            update_fields.append("noted_cash = %s")
            params.append(data['noted_cash'])
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        params.append(user_id)
        
        cursor.execute(f'''
            UPDATE users SET {', '.join(update_fields)}
            WHERE id = %s
        ''', params)
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "User updated successfully"}), 200

    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update user"}), 500

@admin_api.route('/api/admin/table/users/<int:user_id>', methods=['DELETE'])
@admin_required_api
def delete_user_table(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if user has orders
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE user_id = %s", (user_id,))
        order_count = cursor.fetchone()[0]
        
        if order_count > 0:
            return jsonify({
                "success": False, 
                "message": f"Cannot delete user with {order_count} orders."
            }), 400
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "User deleted successfully"}), 200

    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete user"}), 500

# ============================================================================
# ORDERS API ENDPOINTS
# ============================================================================

@admin_api.route('/api/admin/table/orders', methods=['GET'])
@admin_required_api
def get_orders_table():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 25))
        search = request.args.get('search', '')
        filter_value = request.args.get('filter', 'all')
        sort_column = request.args.get('sort_column', 'order_date')
        sort_direction = request.args.get('sort_direction', 'desc')
        
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(users.name LIKE %s OR orders.id LIKE %s)")
            params.extend([f'%{search}%', f'%{search}%'])
        
        if filter_value and filter_value != 'all':
            where_conditions.append("orders.status = %s")
            params.append(filter_value)
        
        where_clause = ''
        if where_conditions:
            where_clause = 'WHERE ' + ' AND '.join(where_conditions)

        # Get total count
        count_query = f'''
            SELECT COUNT(*) as total
            FROM orders
            LEFT JOIN users ON orders.user_id = users.id
            {where_clause}
        '''
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']

        # Main query
        valid_columns = ['id', 'customer_name', 'order_date', 'total', 'status', 'payment_method']
        if sort_column not in valid_columns:
            sort_column = 'order_date'
        if sort_direction not in ['asc', 'desc']:
            sort_direction = 'desc'

        query = f'''
            SELECT 
                orders.id,
                orders.order_date,
                orders.total,
                orders.status,
                orders.payment_method,
                orders.shipping_method,
                users.name as customer_name,
                COUNT(order_items.id) as item_count
            FROM orders
            LEFT JOIN users ON orders.user_id = users.id
            LEFT JOIN order_items ON orders.id = order_items.order_id
            {where_clause}
            GROUP BY orders.id
            ORDER BY {sort_column} {sort_direction}
            LIMIT %s OFFSET %s
        '''
        
        cursor.execute(query, params + [per_page, offset])
        orders = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "data": orders,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }), 200

    except Exception as e:
        print(f"Error fetching orders: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch orders"}), 500

@admin_api.route('/api/admin/orders/<int:order_id>', methods=['GET'])
@admin_required_api
def get_order_details(order_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get order details with customer info
        cursor.execute('''
            SELECT 
                orders.*,
                users.name AS customer_name,
                users.email AS customer_email,
                users.address AS customer_address
            FROM orders
            LEFT JOIN users ON orders.user_id = users.id
            WHERE orders.id = %s
        ''', (order_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({"success": False, "message": "Order not found"}), 404

        # Get order items
        cursor.execute('''
            SELECT 
                order_items.*,
                products.name AS product_name,
                products.price AS product_price
            FROM order_items
            LEFT JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id = %s
        ''', (order_id,))
        order_items = cursor.fetchall()

        order['items'] = order_items
        
        cursor.close()
        connection.close()

        return jsonify({"success": True, "data": order}), 200
    except Exception as e:
        print(f"Error fetching order details: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch order details"}), 500

@admin_api.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
@admin_required_api
def update_order(order_id):
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Track if status is being updated
        status_changed = False
        new_status = None
        if 'status' in data:
            status_changed = True
            new_status = data['status']
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        if 'status' in data:
            update_fields.append("status = %s")
            params.append(data['status'])
        if 'payment_method' in data:
            update_fields.append("payment_method = %s")
            params.append(data['payment_method'])
        if 'shipping_method' in data:
            update_fields.append("shipping_method = %s")
            params.append(data['shipping_method'])
        if 'tracking_number' in data:
            update_fields.append("tracking_number = %s")
            params.append(data['tracking_number'])
        if 'admin_notes' in data:
            update_fields.append("admin_notes = %s")
            params.append(data['admin_notes'])
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        params.append(order_id)
        
        cursor.execute(f'''
            UPDATE orders SET {', '.join(update_fields)}
            WHERE id = %s
        ''', params)
        
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Order not found"}), 404
        
        connection.commit()
        
        # Send email notification if status changed
        if status_changed:
            try:
                # Get user info and order details for email notification
                cursor.execute('''
                    SELECT o.*, u.name AS user_name, u.email AS user_email
                    FROM orders o
                    JOIN users u ON o.user_id = u.id
                    WHERE o.id = %s
                ''', (order_id,))
                order_data = cursor.fetchone()
                
                # Convert to dictionary if it's a tuple
                if order_data and not isinstance(order_data, dict):
                    columns = [col[0] for col in cursor.description]
                    order_data = dict(zip(columns, order_data))
                
                if order_data:
                    from noted.services.email_service import EmailService
                    from noted.models import Order
                    
                    # Create Order object with necessary attributes for email
                    order = Order()
                    order.id = order_data['id']
                    order.order_date = order_data['order_date']
                    order.status = new_status
                    order.shipping_method = order_data.get('shipping_method', '')
                    # Handle potentially missing tracking number
                    order.tracking_number = order_data.get('tracking_number', '')
                    
                    # Add tracking URL if status is 'shipped' and has tracking number
                    tracking_number = order_data.get('tracking_number', '')
                    shipping_method = order_data.get('shipping_method', '').lower()
                    
                    if new_status == 'shipped' and tracking_number:
                        # Generate tracking URL based on shipping method
                        tracking_url = None
                        # For demonstration purposes - adjust these URLs based on actual carriers
                        if 'dhl' in shipping_method:
                            tracking_url = f"https://www.dhl.com/pt-en/home/tracking.html?tracking-id={tracking_number}"
                        elif 'ctt' in shipping_method:
                            tracking_url = f"https://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx?objects={tracking_number}"
                        elif 'fedex' in shipping_method:
                            tracking_url = f"https://www.fedex.com/fedextrack/?trknbr={tracking_number}"
                        else:
                            # Generic tracking URL
                            tracking_url = f"https://t.17track.net/en#nums={tracking_number}"
                        
                        # Set tracking URL
                        order.tracking_url = tracking_url
                        
                        # Update tracking URL in database if not already set
                        tracking_url_in_db = order_data.get('tracking_url', '')
                        if not tracking_url_in_db and tracking_url:
                            try:
                                cursor.execute(
                                    "UPDATE orders SET tracking_url = %s WHERE id = %s", 
                                    (tracking_url, order_id)
                                )
                                connection.commit()
                            except Exception as e:
                                print(f"Failed to update tracking URL: {e}")
                                # Continue even if this fails
                    
                    # Get order items
                    cursor.execute('''
                        SELECT oi.*, p.name, p.image 
                        FROM order_items oi
                        JOIN products p ON oi.product_id = p.id
                        WHERE oi.order_id = %s
                    ''', (order_id,))
                    items_data = cursor.fetchall()
                    
                    # Convert items to dictionaries if they're tuples
                    if items_data and items_data[0] and not isinstance(items_data[0], dict):
                        columns = [col[0] for col in cursor.description]
                        items_data = [dict(zip(columns, item)) for item in items_data]
                    
                    # Create items for the order
                    class OrderItem:
                        pass
                        
                    class Product:
                        pass
                    
                    order.items = []
                    for item_data in items_data:
                        try:
                            item = OrderItem()
                            # Use .get() with defaults to handle missing keys
                            item.quantity = item_data.get('quantity', 1)
                            item.unit_price = item_data.get('unit_price', 0)
                            item.product = Product()
                            item.product.name = item_data.get('name', 'Unknown Product')
                            item.product.image = item_data.get('image', 'default.jpg')
                            order.items.append(item)
                        except Exception as e:
                            print(f"Error creating order item: {e}")
                            # Continue with other items
                    
                    # Send notification email
                    try:
                        user_email = order_data.get('user_email', '')
                        user_name = order_data.get('user_name', '')
                        
                        if not user_email:
                            print(f"Cannot send email: No email address for order {order_id}")
                        else:
                            # Use the unified send_order_email method with status_update type
                            EmailService.send_order_email(
                                user_email,
                                user_name,
                                order,
                                email_type='status_update',
                                include_invoice=False
                            )
                            
                            print(f"Status update email sent successfully to {user_email} for order #{order_id}")
                    except Exception as e:
                        import traceback
                        print(f"Failed to send status notification email: {e}")
                        print(traceback.format_exc())
            except Exception as e:
                import traceback
                print(f"Error preparing email notification: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                # Print the order_data to debug
                if 'order_data' in locals():
                    print(f"Order data type: {type(order_data)}")
                    print(f"Order data keys: {order_data.keys() if isinstance(order_data, dict) else 'Not a dict'}")
        
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Order updated successfully"}), 200

    except Exception as e:
        print(f"Error updating order: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update order"}), 500

@admin_api.route('/api/admin/orders/<int:order_id>/generate-invoice', methods=['POST'])
@admin_required_api
def generate_invoice(order_id):
    """Generate invoice PDF for an order"""
    try:
        from noted.services.invoice_service import InvoiceService
        
        invoice_service = InvoiceService()
        
        # First check if an invoice already exists
        existing_pdf_path = invoice_service.get_invoice_path(order_id)
        if existing_pdf_path:
            # Invoice already exists, return its path
            return jsonify({
                "success": True, 
                "message": "Invoice already exists",
                "pdf_path": existing_pdf_path,
                "regenerated": False
            }), 200
            
        # Generate new invoice
        pdf_path, error = invoice_service.generate_invoice_pdf(order_id)
        
        if error:
            # Check for specific error messages
            if "pdfkit" in error.lower() and "not installed" in error.lower():
                return jsonify({
                    "success": False, 
                    "message": "PDF generation tools are not installed properly. Please run the install_wkhtmltopdf.bat script and restart the server.",
                    "error_details": error
                }), 500
            return jsonify({"success": False, "message": error}), 500
            
        return jsonify({
            "success": True, 
            "message": "Invoice generated successfully",
            "pdf_path": pdf_path,
            "regenerated": True
        }), 200
        
    except ImportError as e:
        error_msg = str(e)
        if "pdfkit" in error_msg.lower():
            return jsonify({
                "success": False, 
                "message": "PDF generation module is not installed. Please run: pip install pdfkit weasyprint reportlab and then run install_wkhtmltopdf.bat",
                "error_details": error_msg
            }), 500
        return jsonify({"success": False, "message": f"Missing module: {error_msg}"}), 500
        
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        return jsonify({"success": False, "message": f"Failed to generate invoice: {str(e)}"}), 500

@admin_api.route('/api/admin/orders/<int:order_id>/send-invoice', methods=['POST'])
@admin_required_api
def send_invoice(order_id):
    """Send invoice PDF by email"""
    try:
        from noted.services.invoice_service import InvoiceService
        
        invoice_service = InvoiceService()
        
        # Check if invoice exists
        invoice_details = invoice_service.get_invoice_details(order_id)
        
        if not invoice_details or not invoice_details.get('pdf_path'):
            # Generate invoice first
            pdf_path, error = invoice_service.generate_invoice_pdf(order_id)
            if error:
                return jsonify({"success": False, "message": f"Failed to generate invoice: {error}"}), 500
            
            # Refresh invoice details after generation
            invoice_details = invoice_service.get_invoice_details(order_id)
            if not invoice_details:
                return jsonify({"success": False, "message": "Failed to retrieve invoice details after generation"}), 500
                
        # Send invoice email
        success, message = invoice_service.send_invoice_email(order_id)
        
        if not success:
            return jsonify({"success": False, "message": message}), 500
            
        return jsonify({
            "success": True, 
            "message": "Invoice sent successfully"
        }), 200
        
    except Exception as e:
        print(f"Error sending invoice: {str(e)}")
        return jsonify({"success": False, "message": f"Failed to send invoice: {str(e)}"}), 500

@admin_api.route('/api/admin/orders/<int:order_id>/invoice-info', methods=['GET'])
@admin_required_api
def get_invoice_info(order_id):
    """Get invoice information for an order"""
    try:
        from noted.services.invoice_service import InvoiceService
        
        invoice_service = InvoiceService()
        invoice_details = invoice_service.get_invoice_details(order_id)
        
        if not invoice_details:
            return jsonify({
                "success": False, 
                "message": "No invoice found for this order",
                "has_invoice": False
            }), 404
            
        return jsonify({
            "success": True,
            "has_invoice": True,
            "invoice": {
                "id": invoice_details['id'],
                "order_id": invoice_details['order_id'],
                "invoice_number": invoice_details['invoice_number'],
                "invoice_date": invoice_details['invoice_date'].strftime('%Y-%m-%d %H:%M:%S') if invoice_details['invoice_date'] else None,
                "pdf_path": invoice_details['pdf_path'],
                "customer_name": invoice_details['customer_name'],
                "customer_email": invoice_details['customer_email'],
                "invoice_sent": invoice_details['invoice_sent'] == 1,
                "invoice_sent_date": invoice_details['invoice_sent_date'].strftime('%Y-%m-%d %H:%M:%S') if invoice_details['invoice_sent_date'] else None,
            }
        }), 200
        
    except Exception as e:
        print(f"Error retrieving invoice info: {str(e)}")
        return jsonify({"success": False, "message": f"Failed to retrieve invoice info: {str(e)}"}), 500

# ============================================================================
# STOCK MANAGEMENT API ENDPOINTS
# ============================================================================

@admin_api.route('/api/admin/stock/<int:product_id>', methods=['GET'])
@admin_required_api
def get_product_stock(product_id):
    """Get stock information for a specific product"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT 
                p.id,
                p.name,
                p.price,
                c.description as category_description,
                COALESCE(ps.quantity, 0) as stock_quantity
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN product_stock ps ON p.id = ps.product_id
            WHERE p.id = %s
        ''', (product_id,))
        
        product = cursor.fetchone()
        
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "data": product
        }), 200
        
    except Exception as e:
        print(f"Error fetching product stock: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch product stock"}), 500

@admin_api.route('/api/admin/stock/<int:product_id>', methods=['PUT'])
@admin_required_api
def update_product_stock(product_id):
    """Update stock for a specific product"""
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        reason = data.get('reason', 'manual_adjustment')
        
        if quantity is None or quantity < 0:
            return jsonify({"success": False, "message": "Valid quantity is required"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if product exists
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        # Update or insert stock record
        cursor.execute('''
            INSERT INTO product_stock (product_id, quantity) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE quantity = VALUES(quantity)
        ''', (product_id, quantity))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": f"Stock updated to {quantity} units"
        }), 200
        
    except Exception as e:
        print(f"Error updating product stock: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update stock"}), 500

@admin_api.route('/api/admin/stock/bulk-update', methods=['POST'])
@admin_required_api
def bulk_update_stock():
    """Update stock for multiple products"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Handle both old format (updates array) and new format (product_ids, operation, quantity)
        updates = []
        
        if 'updates' in data:
            # Old format: direct updates array
            updates = data.get('updates', [])
        elif 'product_ids' in data and 'operation' in data and 'quantity' in data:
            # New format: product_ids with operation
            product_ids = data.get('product_ids', [])
            operation = data.get('operation', 'set')
            quantity = data.get('quantity', 0)
            reason = data.get('reason', '')
            
            if not product_ids:
                return jsonify({"success": False, "message": "No product IDs provided"}), 400
            
            # Convert to updates format based on operation
            for product_id in product_ids:
                if operation == 'set':
                    # Set to specific value
                    updates.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'reason': reason
                    })
                elif operation == 'add':
                    # Add to current stock - we'll need to fetch current values
                    updates.append({
                        'product_id': product_id,
                        'quantity_change': quantity,
                        'operation': 'add',
                        'reason': reason
                    })
                elif operation == 'subtract':
                    # Subtract from current stock
                    updates.append({
                        'product_id': product_id,
                        'quantity_change': -quantity,
                        'operation': 'add',  # We'll use add with negative value
                        'reason': reason
                    })
        else:
            return jsonify({"success": False, "message": "No updates provided"}), 400
        
        if not updates:
            return jsonify({"success": False, "message": "No updates provided"}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get current stock values for operations that need them
        product_ids = [update['product_id'] for update in updates]
        
        # Validate all product IDs exist and get current stock
        placeholders = ','.join(['%s'] * len(product_ids))
        cursor.execute(f'''
            SELECT p.id, COALESCE(ps.quantity, 0) as current_stock 
            FROM products p 
            LEFT JOIN product_stock ps ON p.id = ps.product_id 
            WHERE p.id IN ({placeholders})
        ''', product_ids)
        
        current_stock = {row[0]: row[1] for row in cursor.fetchall()}
        existing_ids = set(current_stock.keys())
        invalid_ids = [pid for pid in product_ids if pid not in existing_ids]
        
        if invalid_ids:
            cursor.close()
            connection.close()
            return jsonify({
                "success": False, 
                "message": f"Invalid product IDs: {invalid_ids}"
            }), 400
        
        # Process updates
        successful_updates = 0
        for update in updates:
            product_id = update['product_id']
            
            if 'operation' in update and update['operation'] == 'add':
                # Add/subtract operation
                current_qty = current_stock.get(product_id, 0)
                new_quantity = max(0, current_qty + update['quantity_change'])
            else:
                # Set operation (default)
                new_quantity = max(0, update['quantity'])
            
            try:
                cursor.execute('''
                    INSERT INTO product_stock (product_id, quantity) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE quantity = VALUES(quantity)
                ''', (product_id, new_quantity))
                successful_updates += 1
            except Exception as e:
                print(f"Error updating product {product_id}: {str(e)}")
                continue
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "message": f"Updated stock for {successful_updates} products"
        }), 200
        
    except Exception as e:
        print(f"Error bulk updating stock: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update stock"}), 500

@admin_api.route('/api/admin/stock/summary', methods=['GET'])
@admin_required_api
def get_stock_summary():
    """Get stock summary statistics"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get stock statistics
        cursor.execute('''
            SELECT 
                COUNT(p.id) as total_products,
                COUNT(CASE WHEN COALESCE(ps.quantity, 0) > 0 THEN 1 END) as products_in_stock,
                COUNT(CASE WHEN COALESCE(ps.quantity, 0) = 0 THEN 1 END) as products_out_of_stock,
                COUNT(CASE WHEN COALESCE(ps.quantity, 0) > 0 AND COALESCE(ps.quantity, 0) <= 10 THEN 1 END) as products_low_stock,
                SUM(COALESCE(ps.quantity, 0)) as total_stock_units
            FROM products p
            LEFT JOIN product_stock ps ON p.id = ps.product_id
        ''')
        
        summary = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "data": summary
        }), 200
        
    except Exception as e:
        print(f"Error fetching stock summary: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch stock summary"}), 500

@admin_api.errorhandler(500)
def handle_internal_server_error(e):
    """Handle 500 errors with JSON response for API endpoints"""
    import traceback
    error_traceback = traceback.format_exc()
    print("API ERROR:", error_traceback)
    
    return jsonify({
        "success": False,
        "message": "Internal server error. Check server logs for details.",
        "error_type": str(type(e).__name__) if isinstance(e, Exception) else "Unknown",
        "error_detail": str(e) if isinstance(e, Exception) else "No details available"
    }), 500


# API Routes below this point
