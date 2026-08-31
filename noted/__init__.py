from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os
import secrets

db = SQLAlchemy()
mail = Mail()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    # Generate a strong secret key if not set
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    # Explicitly set SQLALCHEMY_TRACK_MODIFICATIONS to suppress warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Use FLASK_DEBUG instead of FLASK_ENV
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'
    # Make sessions more secure
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24 * 7  # 7 days
    app.config['SESSION_USE_SIGNER'] = True
    
    # Existing mail config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 25))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

    db.init_app(app)
    mail.init_app(app)

    # Importar e registar os blueprints
    from noted.routes import auth_bp, cart_bp, checkout_bp, misc_bp, products_bp, admin_bp, orders_bp
    from noted.routes.email_preview import email_preview_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(email_preview_bp)
    
    from noted.routes.api.admin_api import admin_api
    from noted.routes.api.products_api import products_api
    app.register_blueprint(admin_api)
    app.register_blueprint(products_api)

    # Context processor for user information
    @app.context_processor
    def inject_user():
        from flask import session
        from noted.models import User
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return dict(current_user=user)
        
    # Context processor for categories - make available globally
    @app.context_processor
    def inject_categories():
        from noted.models import Category
        return {'categories': Category.query.all()}


    return app
