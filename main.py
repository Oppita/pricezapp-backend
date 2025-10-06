from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI()

# ====== CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ puedes restringirlo más adelante
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Seguridad ======
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ====== Simulación de base de datos ======
fake_users_db = {}

# ====== Modelos ======
class User(BaseModel):
    name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

# ====== Rutas ======

@app.get("/")
def root():
    return {"status": "ok", "message": "PriceZapp backend running"}

@app.post("/auth/register")
def register_user(user: User):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = pwd_context.hash(user.password)
    fake_users_db[user.email] = {"name": user.name, "password": hashed_password}
    return {"message": "User created successfully"}

@app.post("/auth/login")
def login_user(login: LoginData):
    user = fake_users_db.get(login.email)
    if not user or not pwd_context.verify(login.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": login.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
