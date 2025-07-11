from flask import Blueprint, jsonify, request
from ...models import db, Product, Category, ProductCollection

products_api = Blueprint('products_api', __name__)

@products_api.route('/api/products/collections', methods=['GET'])
def products_by_collection():
    """Get all products organized by collection"""
    collections = ProductCollection.query.all()
    
    result = []
    
    # Get all products without collection
    no_collection_products = Product.query.filter(Product.collection_id.is_(None)).all()
    if no_collection_products:
        result.append({
            'collection': {
                'id': None,
                'name': 'No Collection' 
            },
            'products': [{
                'id': p.id,
                'name': p.name,
                'collection_id': p.collection_id
            } for p in no_collection_products]
        })
    
    # Get products by collection
    for collection in collections:
        collection_products = Product.query.filter_by(collection_id=collection.id).all()
        result.append({
            'collection': {
                'id': collection.id,
                'name': collection.name
            },
            'products': [{
                'id': p.id,
                'name': p.name,
                'collection_id': p.collection_id
            } for p in collection_products]
        })
    
    return jsonify(result)

@products_api.route('/api/products/<int:product_id>/related', methods=['GET'])
def get_related_products(product_id):
    """Get related products for a specific product"""
    product = Product.query.get_or_404(product_id)
    
    if not product.collection_id:
        return jsonify([])
    
    related = Product.query.filter(
        Product.collection_id == product.collection_id,
        Product.id != product.id
    ).all()
    
    return jsonify([{
        'id': p.id, 
        'name': p.name,
        'image': p.image,
        'price': float(p.price),
        'collection_id': p.collection_id
    } for p in related])
