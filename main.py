# ====== PriceZapp Backend - main.py ======
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# ====== Inicialización ======
app = FastAPI(title="PriceZapp API", version="1.0")

# ====== Configuración de CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ puedes poner el dominio de tu frontend si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Seguridad ======
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ====== Base de datos simulada ======
fake_users_db = {}

# ====== Modelos ======
class User(BaseModel):
    name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

# ====== Funciones auxiliares ======
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ====== Endpoints ======
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

    access_token = create_access_token({"sub": login.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ====== Verificación simple ======
@app.get("/auth/users")
def list_users():
    return {"users": list(fake_users_db.keys())}
