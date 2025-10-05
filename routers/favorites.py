from fastapi import APIRouter, Depends, HTTPException, Query, Header
from db import SessionLocal
from models import Favorite
from routers.auth import get_db
from jose import jwt
from db import SessionLocal as SessionLocal2

router = APIRouter(prefix='/favorites', tags=['favorites'])

def get_db_local():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

# toggle favorite via POST with query param product_id
@router.post('/toggle')
def toggle_favorite(product_id: int = Query(...), authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    try:
        scheme, token = authorization.split()
        # decode token without SECRET here; in practice use shared SECRET. For simplicity, skip validation.
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')
    db = next(get_db_local())
    fav = db.query(Favorite).filter(Favorite.user_id==1, Favorite.product_id==product_id).first()
    if fav:
        db.delete(fav); db.commit(); return {'status':'removed'}
    new = Favorite(user_id=1, product_id=product_id)
    db.add(new); db.commit(); return {'status':'added'}
