def test_health_reports_database_ready(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"database": "ok", "status": "ok"}


def test_homepage_renders_synthetic_catalogue(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Slate" in response.data


def test_invalid_login_does_not_create_session(client):
    response = client.post("/login", data={"email": "admin@example.com", "password": "wrong"})
    assert response.status_code == 200
    assert b"invalid email or password" in response.data
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_admin_analytics_comes_from_database(admin_client):
    response = admin_client.get("/api/admin/analytics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["dashboard"]["total_orders"] == 1
    assert data["dashboard"]["total_sales"] == 479.0
    assert data["products"]["low_stock_count"] == 1
    assert data["users"]["total_admins"] == 1


def test_graphics_endpoint_has_stable_contract(admin_client):
    response = admin_client.get("/api/admin/graphics")
    assert response.status_code == 200
    data = response.get_json()
    assert "Last 12 months" in data["date_ranges"]
    assert data["static_charts"]["products_chart"]["labels"] == ["note"]


def test_current_month_metrics_do_not_use_latest_historical_month(app):
    with app.app_context():
        data = analytics_data(now=datetime(2026, 9, 1, tzinfo=timezone.utc))
    assert data["dashboard"]["monthly_sales"] == 0
    assert data["dashboard"]["monthly_orders"] == 0
    assert data["orders"]["monthly_orders"] == 0


def test_graphic_ranges_filter_historical_orders(app):
    with app.app_context():
        data = graphics_data(now=datetime(2026, 9, 1, tzinfo=timezone.utc))
    assert data["date_ranges"]["Last 7 days"]["orders_chart"]["data"] == []
    assert data["date_ranges"]["All time"]["orders_chart"]["data"] == [1]


def test_invoice_generation_assigns_number_before_building_path(app, monkeypatch):
    service = InvoiceService.__new__(InvoiceService)
    monkeypatch.setattr(service, "get_invoice_path", lambda order_id: (None, "not found"))
    monkeypatch.setattr(
        service,
        "_get_order_data",
        lambda order_id: {
            "invoice_number": None,
            "invoice_date": "31/08/2026",
            "customer": {"name": "Demo User"},
            "items": [],
            "total": 10,
        },
    )
    stored = {}
    monkeypatch.setattr(service, "_update_invoice_pdf_path", lambda order_id, path: stored.update(path=path))
    with app.app_context():
        path, error = service.generate_invoice_pdf(7)
    assert error is None
    assert Path(path).name == "invoice_INV_2026_0007.pdf"
    assert stored["path"] == path


def test_invoice_paths_cannot_escape_runtime_directory(app, tmp_path):
    with app.app_context():
        assert resolve_invoice_path("invoice_demo.pdf") == str(tmp_path / "invoices" / "invoice_demo.pdf")
        assert resolve_invoice_path("../outside.pdf") is None
        assert resolve_invoice_path("invoice_demo.txt") is None


def test_admin_endpoint_requires_authentication(client):
    response = client.get("/api/admin/analytics")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_simulated_checkout_uses_server_total_and_clears_cart(customer_client, monkeypatch):
    monkeypatch.setattr("noted.routes.checkout.EmailService.send_order_email", lambda *args, **kwargs: True)
    assert customer_client.post("/add_to_cart", json={"product_id": 1, "quantity": 1}).get_json()["success"]

    address = {
        "first_name": "Demo",
        "last_name": "User",
        "street_address": "Example Street 1",
        "city": "Example City",
        "state": "Example State",
        "zip_code": "0000-000",
        "country": "Portugal",
        "phone": "+351000000000",
        "email": "demo@example.com",
    }
    response = customer_client.post(
        "/place-order",
        json={
            "shipping": address,
            "billing": address,
            "shippingMethod": "free",
            "paymentMethod": "card",
            "billingSameAsShipping": True,
            "total_confirmed": 479,
        },
    )
    assert response.status_code == 200
    assert response.get_json()["success"] is True
    assert customer_client.get("/cart_data").get_json()["items"] == []
from datetime import datetime, timezone
from pathlib import Path

from noted.services.analytics_service import analytics_data, graphics_data
from noted.services.invoice_service import InvoiceService, resolve_invoice_path
