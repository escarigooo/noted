from datetime import datetime
from noted import db
import mysql.connector

def get_db_connection():
    """
    Create and return a new MySQL database connection.
    Used for raw SQL queries when SQLAlchemy ORM is not suitable.
    """
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

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('product_collections.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    features = db.relationship('ProductFeature', backref='product', cascade="all, delete-orphan")
    images = db.relationship('ProductImage', backref='product', cascade="all, delete-orphan")
    accessories = db.relationship('Accessory', secondary='product_accessories', backref='products')

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))

class Accessory(db.Model):
    __tablename__ = 'accessories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(200))

# Association table for product-accessory relationship
product_accessories = db.Table('product_accessories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('accessory_id', db.Integer, db.ForeignKey('accessories.id'), primary_key=True)
)

class FeatureType(db.Model):
    __tablename__ = 'feature_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class ProductFeature(db.Model):
    __tablename__ = 'product_features'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    feature_type_id = db.Column(db.Integer, db.ForeignKey('feature_types.id', ondelete="CASCADE"), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    feature_type = db.relationship('FeatureType')
    
    def get_feature_type_name(self):
        """Safely get feature type name, handling None values."""
        if self.feature_type and hasattr(self.feature_type, 'name'):
            return self.feature_type.name
        return "Unknown"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    role = db.Column(db.Integer, default=2)  # 1 = admin, 2 = customer
    noted_cash = db.Column(db.Numeric(10, 2), default=0.00)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product')

class Discount(db.Model):
    __tablename__ = 'discounts'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # ex: 10.00
    is_percentage = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2))  # Changed from Float to Numeric for precision
    shipping_method = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))
    billing_same_as_shipping = db.Column(db.Boolean)

    user = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan")
    shipping_address = db.relationship('ShippingAddress', backref='order', uselist=False, cascade="all, delete-orphan")
    billing_address = db.relationship('BillingAddress', backref='order', uselist=False, cascade="all, delete-orphan")
    payment_info = db.relationship('PaymentInfo', backref='order', uselist=False, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Changed from Float to Numeric for precision

    product = db.relationship('Product')

class ShippingAddress(db.Model):
    __tablename__ = 'shipping_addresses'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    street_address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class BillingAddress(db.Model):
    __tablename__ = 'billing_addresses'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    street_address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class PaymentInfo(db.Model):
    __tablename__ = 'payment_info'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    card_last4 = db.Column(db.String(4))
    card_brand = db.Column(db.String(50))
    paid = db.Column(db.Boolean, default=False)
    payment_date = db.Column(db.DateTime)

class NotedCashTransaction(db.Model):
    __tablename__ = 'noted_cash_transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    change_amount = db.Column(db.Numeric(10, 2), nullable=False)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Adicione esta classe ao final do arquivo

class ProductCollection(db.Model):
    __tablename__ = 'product_collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relação many-to-many com produtos
    products = db.relationship('Product', 
                              secondary='collection_products', 
                              backref=db.backref('collections', lazy='dynamic'))

# Tabela de associação para collection-product
collection_products = db.Table('collection_products',
    db.Column('collection_id', db.Integer, db.ForeignKey('product_collections.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)