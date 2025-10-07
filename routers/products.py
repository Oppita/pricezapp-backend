# routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Product, Category, Price
from typing import List, Optional

router = APIRouter(prefix='/products', tags=['products'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[dict])
def list_products(q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Product)
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    products = query.limit(200).all()
    result = []
    for product in products:
        prices = db.query(Price).filter(Price.product_id == product.id).all()
        result.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'brand': product.brand,
            'image': product.image,
            'rating': product.rating,
            'category_id': product.category_id,
            'supermarkets': [ { 'name': p.supermarket, 'price': p.price, 'previousPrice': p.previous_price, 'delivery': p.delivery } for p in prices ]
        })
    return result

@router.get('/{product_id}', response_model=dict)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    prices = db.query(Price).filter(Price.product_id == product.id).all()
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'brand': product.brand,
        'image': product.image,
        'rating': product.rating,
        'category_id': product.category_id,
        'supermarkets': [ { 'name': p.supermarket, 'price': p.price, 'previousPrice': p.previous_price, 'delivery': p.delivery } for p in prices ]
    }

@router.get('/categories/', response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).all()
    return [ { 'id': c.id, 'name': c.name, 'parent_id': c.parent_id, 'icon': c.icon, 'color': c.color } for c in cats ]

