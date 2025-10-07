# routers/favorites.py
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Favorite, Product, Price
from routers.auth import get_current_user_id

router = APIRouter(prefix="/favorites", tags=["favorites"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/toggle")
def toggle_favorite(product_id: int = Query(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    fav = db.query(Favorite).filter(Favorite.user_id==user_id, Favorite.product_id==product_id).first()
    if fav:
        db.delete(fav); db.commit(); return {"status":"removed"}
    new = Favorite(user_id=user_id, product_id=product_id)
    db.add(new); db.commit(); return {"status":"added"}

@router.get("/")
def get_favorites(authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    product_ids = [f.product_id for f in favorites]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
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
            'supermarkets': [ { 'name': p.supermarket, 'price': p.price, 'previousPrice': p.previous_price, 'delivery': p.delivery } for p in prices ]
        })
    return result
