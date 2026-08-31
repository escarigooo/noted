from collections import defaultdict
from datetime import datetime, timedelta, timezone

from noted.models import Category, Order, PaymentInfo, Product, ProductStock, User


def _money(value):
    return float(value or 0)


def _monthly_series(orders):
    sales = defaultdict(float)
    counts = defaultdict(int)
    for order in orders:
        if not order.order_date:
            continue
        key = order.order_date.strftime("%Y-%m")
        sales[key] += _money(order.total)
        counts[key] += 1
    labels = sorted(sales)
    return labels, [round(sales[key], 2) for key in labels], [counts[key] for key in labels]


def _as_utc(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _orders_since(orders, since):
    return [
        order
        for order in orders
        if order.order_date and _as_utc(order.order_date) >= since
    ]


def _chart_data(orders):
    labels, sales, counts = _monthly_series(orders)
    return {
        "sales_chart": {
            "labels": labels,
            "data": sales,
            "type": "line",
            "title": "Sales by month",
        },
        "orders_chart": {
            "labels": labels,
            "data": counts,
            "type": "bar",
            "title": "Orders by month",
        },
    }


def analytics_data(now=None):
    orders = Order.query.order_by(Order.order_date.asc()).all()
    users = User.query.all()
    products = Product.query.all()
    stocks = ProductStock.query.all()
    paid_order_ids = {row.order_id for row in PaymentInfo.query.filter_by(paid=True).all()}
    labels, sales, order_counts = _monthly_series(orders)
    total_sales = round(sum(_money(order.total) for order in orders), 2)
    now = now or datetime.now(timezone.utc)
    current_month = now.strftime("%Y-%m")
    monthly_sales = round(
        sum(_money(order.total) for order in orders if order.order_date and order.order_date.strftime("%Y-%m") == current_month),
        2,
    )
    monthly_orders = sum(
        bool(order.order_date and order.order_date.strftime("%Y-%m") == current_month)
        for order in orders
    )
    recent = sorted(orders, key=lambda order: order.order_date or datetime.min, reverse=True)[:10]

    return {
        "last_updated": now.isoformat(),
        "dashboard": {
            "total_sales": total_sales,
            "monthly_sales": monthly_sales,
            "total_orders": len(orders),
            "monthly_orders": monthly_orders,
            "total_customers": sum(user.role == 2 for user in users),
            "active_products": len(products),
            "revenue_growth": 0,
            "recent_orders": [
                {
                    "id": order.id,
                    "customer": order.user.name if order.user else "Guest",
                    "total": _money(order.total),
                    "date": order.order_date.isoformat() if order.order_date else None,
                    "paid": order.id in paid_order_ids,
                }
                for order in recent
            ],
        },
        "products": {
            "total_products": len(products),
            "total_categories": Category.query.count(),
            "out_of_stock_count": sum(stock.quantity == 0 for stock in stocks),
            "low_stock_count": sum(0 < stock.quantity <= 10 for stock in stocks),
        },
        "orders": {
            "total_orders": len(orders),
            "monthly_orders": monthly_orders,
            "paid_orders": len(paid_order_ids),
            "unpaid_orders": len(orders) - len(paid_order_ids),
            "orders_by_month": [{"month": label, "count": count} for label, count in zip(labels, order_counts)],
        },
        "users": {
            "total_users": len(users),
            "total_customers": sum(user.role == 2 for user in users),
            "total_admins": sum(user.role == 1 for user in users),
            "users_with_orders": len({order.user_id for order in orders if order.user_id}),
        },
        "analytics": {
            "sales_by_month": [{"month": label, "sales": value} for label, value in zip(labels, sales)],
            "orders_by_day": [],
            "top_products": [],
            "customer_analytics": [],
            "payment_methods": [],
            "monthly_revenue": sales,
        },
    }


def graphics_data(now=None):
    now = now or datetime.now(timezone.utc)
    data = analytics_data(now=now)
    orders = Order.query.order_by(Order.order_date.asc()).all()
    all_time = _chart_data(orders)
    category_rows = (
        Category.query.outerjoin(Product)
        .with_entities(Category.description, Product.id)
        .all()
    )
    category_counts = defaultdict(int)
    for category, product_id in category_rows:
        if product_id is not None:
            category_counts[category] += 1
    range_days = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 3 months": 90,
        "Last 12 months": 365,
    }
    date_ranges = {
        name: _chart_data(_orders_since(orders, now - timedelta(days=days)))
        for name, days in range_days.items()
    }
    date_ranges["All time"] = all_time
    ranges = [*range_days, "All time"]
    return {
        "last_updated": data["last_updated"],
        "date_ranges": date_ranges,
        "static_charts": {
            "products_chart": {
                "labels": list(category_counts),
                "data": list(category_counts.values()),
                "type": "doughnut",
                "title": "Products by category",
            },
            "top_customers": {"labels": [], "data": [], "type": "bar", "title": "Top customers"},
        },
        "filters": {"date_ranges": ranges, "categories": list(category_counts)},
        "sales_chart": all_time["sales_chart"],
        "orders_chart": all_time["orders_chart"],
    }
