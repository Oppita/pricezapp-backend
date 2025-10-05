from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User
from schemas import UserCreate, UserOut, Token, UserLogin
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = 'CHANGE_ME_SECRET_KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

router = APIRouter(prefix='/auth', tags=['auth'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/register', response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed = get_password_hash(payload.password)
    user = User(name=payload.name, email=payload.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect password')
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'sub': str(user.id), 'exp': datetime.utcnow() + expires}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/me', response_model=UserOut)
def me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    try:
        scheme, token = authorization.split()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get('sub'))
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
