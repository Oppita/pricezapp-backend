# routers/alerts.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Alert
from schemas import AlertCreate
from routers.auth import get_current_user_id

router = APIRouter(prefix="/alerts", tags=["alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_alert(payload: AlertCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    new_alert = Alert(user_id=user_id, product_id=payload.product_id, target_price=payload.target_price)
    db.add(new_alert); db.commit(); db.refresh(new_alert)
    return {"status":"created","alert":new_alert}

@router.get("/")
def get_alerts(authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    alerts = db.query(Alert).filter(Alert.user_id == user_id, Alert.active == True).all()
    return alerts

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    user_id = get_current_user_id(authorization, db)
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == user_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert); db.commit()
    return {"status":"deleted"}
