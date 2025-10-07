# routers/lists.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db import SessionLocal
from models import ShoppingList
from schemas import ShoppingListCreate
from routers.auth import get_current_user_id

router = APIRouter(prefix="/lists", tags=["lists"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_list(payload: ShoppingListCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    new_list = ShoppingList(user_id=user_id, name=payload.name, items=payload.items)
    db.add(new_list); db.commit(); db.refresh(new_list)
    return {"status":"created","list":new_list}

@router.get("/")
def get_lists(authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    lists = db.query(ShoppingList).filter(ShoppingList.user_id == user_id).all()
    return lists

@router.put("/{list_id}")
def update_list(list_id: int, payload: ShoppingListCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id==list_id, ShoppingList.user_id==user_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="List not found")
    shopping_list.name = payload.name
    shopping_list.items = payload.items
    db.commit()
    return {"status":"updated"}

@router.delete("/{list_id}")
def delete_list(list_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id==list_id, ShoppingList.user_id==user_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="List not found")
    db.delete(shopping_list); db.commit()
    return {"status":"deleted"}
