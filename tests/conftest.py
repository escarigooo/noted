from datetime import datetime

import pytest
from werkzeug.security import generate_password_hash

from noted import create_app, db
from noted.models import Category, Order, PaymentInfo, Product, ProductStock, User


@pytest.fixture()
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-only-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "MAIL_SUPPRESS_SEND": True,
            "INVOICE_DIR": str(tmp_path / "invoices"),
        }
    )
    with application.app_context():
        db.create_all()
        category = Category(description="note")
        db.session.add(category)
        db.session.flush()
        product = Product(name="Slate", description="Demo tablet", price=479, image="tablet.png", category_id=category.id)
        admin = User(
            name="Demo Admin",
            email="admin@example.com",
            password=generate_password_hash("DemoOnly!2026", method="pbkdf2:sha256"),
            email_verified=True,
            role=1,
        )
        customer = User(
            name="Demo User",
            email="demo@example.com",
            password=generate_password_hash("DemoOnly!2026", method="pbkdf2:sha256"),
            email_verified=True,
            role=2,
        )
        db.session.add_all([product, admin, customer])
        db.session.flush()
        db.session.add(ProductStock(product_id=product.id, quantity=5))
        order = Order(user_id=customer.id, order_date=datetime(2026, 8, 1), total=479)
        db.session.add(order)
        db.session.flush()
        db.session.add(PaymentInfo(order_id=order.id, paid=True))
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_client(client):
    response = client.post(
        "/login",
        data={"email": "admin@example.com", "password": "DemoOnly!2026"},
    )
    assert response.status_code == 302
    return client


@pytest.fixture()
def customer_client(client):
    response = client.post(
        "/login",
        data={"email": "demo@example.com", "password": "DemoOnly!2026"},
    )
    assert response.status_code == 302
    return client
