from flask import Flask, jsonify
from sqlalchemy import text
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from noted.config import Config


db = SQLAlchemy()
mail = Mail()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set")

    db.init_app(app)
    mail.init_app(app)

    from noted.routes import (
        admin_bp,
        auth_bp,
        cart_bp,
        checkout_bp,
        misc_bp,
        orders_bp,
        products_bp,
    )
    from noted.routes.email_preview import email_preview_bp
    from noted.routes.api.admin_api import admin_api
    from noted.routes.api.products_api import products_api

    for blueprint in (
        auth_bp,
        cart_bp,
        checkout_bp,
        misc_bp,
        products_bp,
        admin_bp,
        orders_bp,
        email_preview_bp,
        admin_api,
        products_api,
    ):
        app.register_blueprint(blueprint)

    @app.context_processor
    def inject_user():
        from flask import session
        from noted.models import User

        user = User.query.get(session["user_id"]) if "user_id" in session else None
        return {"current_user": user}

    @app.context_processor
    def inject_categories():
        from noted.models import Category

        return {"categories": Category.query.all()}

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            app.logger.exception("Database health check failed")
            return jsonify(status="unhealthy", database="unavailable"), 503
        return jsonify(status="ok", database="ok"), 200

    return app
