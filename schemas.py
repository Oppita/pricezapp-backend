from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[float] = 0.0
    category_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class PriceIn(BaseModel):
    supermarket: str
    price: float
    previous_price: Optional[float] = None
    delivery: Optional[str] = None

class ShoppingListCreate(BaseModel):
    name: str
    items: List[Any] = []

class AlertCreate(BaseModel):
    product_id: int
    target_price: float
