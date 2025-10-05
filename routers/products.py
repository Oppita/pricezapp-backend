from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Product, Category
from schemas import ProductOut, ProductBase, CategoryOut, CategoryBase
from typing import List, Optional

router = APIRouter(prefix='/products', tags=['products'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[ProductOut])
def list_products(q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Product)
    if q:
        query = query.filter(Product.name.contains(q))
    return query.limit(200).all()

@router.get('/{product_id}', response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail='Product not found')
    return prod

@router.get('/categories', response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).all()
    return cats

@router.post('/categories', response_model=CategoryOut)
def create_category(cat: CategoryBase, db: Session = Depends(get_db)):
    db_cat = Category(name=cat.name, parent_id=cat.parent_id, icon=cat.icon, color=cat.color)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat
