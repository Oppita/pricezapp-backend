from fastapi import APIRouter, Depends, HTTPException, Header
from db import SessionLocal
from models import Alert
from schemas import AlertCreate
from db import SessionLocal as SessionLocal2

router = APIRouter(prefix='/alerts', tags=['alerts'])

def get_db_local():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
def create_alert(payload: AlertCreate, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    db = next(get_db_local())
    a = Alert(user_id=1, product_id=payload.product_id, target_price=payload.target_price)
    db.add(a); db.commit(); db.refresh(a)
    return a
