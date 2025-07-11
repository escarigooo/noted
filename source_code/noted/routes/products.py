# noted/routes/products.py

from flask import Blueprint, render_template, url_for, request, redirect, flash
from ..models import db, Product, Category, ProductCollection

products_bp = Blueprint('products', __name__)

@products_bp.context_processor
def inject_categories():
    # Disponibilizar categorias em todos os templates que usam este blueprint
    return {'categories': Category.query.all()}

@products_bp.route('/categories')
def categories():
    breadcrumbs = [
        {'label': 'home', 'url': url_for('misc.index')},
        {'label': 'categories', 'url': None}
    ]
    all_categories = Category.query.all()
    return render_template(
        'pages/categories/categories.html',
        categories=all_categories,
        breadcrumbs=breadcrumbs
    )

@products_bp.route('/category/<string:category_name>')
def category_products(category_name):
    category = Category.query.filter_by(description=category_name).first_or_404()
    breadcrumbs = [
        {'label': 'home', 'url': url_for('misc.index')},
        {'label': 'categories', 'url': url_for('products.categories')},
        {'label': category.description, 'url': None}
    ]
    return render_template(
        'pages/categories/category_products.html',
        category=category,
        breadcrumbs=breadcrumbs
    )

@products_bp.route('/product/<product_name>')
def product_details(product_name):
    # Busca o produto pelo nome
    product = Product.query.filter_by(name=product_name).first_or_404()
    category = product.category
    
    # Build breadcrumbs with null check for category
    breadcrumbs = [
        {'label': 'home', 'url': url_for('misc.index')},
        {'label': 'categories', 'url': url_for('products.categories')},
    ]
    
    # Only add category breadcrumb if category exists
    if category:
        breadcrumbs.append({
            'label': category.description,
            'url': url_for('products.category_products', category_name=category.description)
        })
    
    breadcrumbs.append({'label': product.name, 'url': None})
    
    return render_template(
        'pages/products/product_detail.html',
        product=product,
        breadcrumbs=breadcrumbs,
        get_related_products=get_related_products  # Certifique-se de passar esta função
    )

@products_bp.route('/product/id/<int:product_id>')
def product_details_by_id(product_id):
    product = Product.query.get_or_404(product_id)
    category = product.category
    
    # Build breadcrumbs with null check for category
    breadcrumbs = [
        {'label': 'home', 'url': url_for('misc.index')},
        {'label': 'categories', 'url': url_for('products.categories')},
    ]
    
    # Only add category breadcrumb if category exists
    if category:
        breadcrumbs.append({
            'label': category.description,
            'url': url_for('products.category_products', category_name=category.description)
        })
    
    breadcrumbs.append({'label': product.name, 'url': None})
    
    return render_template(
        'pages/products/product_detail.html',
        product=product,
        category=category,
        breadcrumbs=breadcrumbs,
        get_related_products=get_related_products  # Pass the function to the template
    )

def get_related_products(collection_id, current_product_id, limit=8):
    """Buscar produtos relacionados da mesma coleção, excluindo o produto atual"""
    print(f"Getting related products: Collection ID={collection_id}, Current Product ID={current_product_id}")
    
    if not collection_id:
        print("No collection ID provided, returning empty list")
        return []
    
    related_products = Product.query.filter(
        Product.collection_id == collection_id,
        Product.id != current_product_id
    ).limit(limit).all()
    
    print(f"Found {len(related_products)} related products")
    for product in related_products:
        print(f"  - {product.name} (ID: {product.id})")
    
    return related_products
