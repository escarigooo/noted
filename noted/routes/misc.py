from flask import Blueprint, render_template, current_app
from ..models import Product
import json
import os

misc_bp = Blueprint('misc', __name__)

@misc_bp.route('/')
def index():
    products = Product.query.all()
    
    # Load analytics data from JSON file
    analytics_path = os.path.join(current_app.static_folder, 'data', 'analytics.json')
    analytics_data = {}
    
    try:
        if os.path.exists(analytics_path):
            with open(analytics_path, 'r') as f:
                analytics_data = json.load(f)
    except Exception as e:
        print(f"Error loading analytics data: {e}")
    
    return render_template("pages/index.html", products=products, analytics=analytics_data)

@misc_bp.route('/resources')
def resources():
    return render_template("pages/info/resources.html")

@misc_bp.route('/download')
def download():
    return render_template("pages/info/download.html")

@misc_bp.route('/support')
def support():
    return render_template("pages/info/support.html")

@misc_bp.route('/about')
def about():
    return render_template("pages/info/about.html")

@misc_bp.route('/terms')
def terms():
    return render_template("pages/info/terms.html")
