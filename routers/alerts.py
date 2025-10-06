from fastapi import APIRouter, Depends, HTTPException, Header
from db import SessionLocal
from models import Alert
from schemas import AlertCreate

router = APIRouter(prefix="/alerts", tags=["alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_alert(payload: AlertCreate, db=Depends(get_db), authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    new_alert = Alert(user_id=1, product_id=payload.product_id, target_price=payload.target_price)
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return {"status": "created", "alert": new_alert}

@router.get("/")
def list_alerts(db=Depends(get_db)):
    return db.query(Alert).all()
