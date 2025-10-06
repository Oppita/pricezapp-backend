from fastapi import FastAPI
from db import engine, Base
from routers import auth, products, favorites, lists, alerts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PRICEZAPP Backend (Auth Ready)")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiarlo a tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(lists.router, prefix="/lists", tags=["Lists"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

@app.get("/")
def root():
    return {"message": "PRICEZAPP backend (auth) running"}

