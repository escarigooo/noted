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
