from fastapi import APIRouter, Depends, HTTPException, Header
from db import SessionLocal
from schemas import ShoppingListCreate
from models import ShoppingList
from jose import jwt
from db import SessionLocal as SessionLocal2

router = APIRouter(prefix='/lists', tags=['lists'])

def get_db_local():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
def create_list(payload: ShoppingListCreate, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    # naive user extraction for scaffold: user_id = 1
    db = next(get_db_local())
    nl = ShoppingList(user_id=1, name=payload.name, items=payload.items)
    db.add(nl); db.commit(); db.refresh(nl)
    return nl
