from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ProductCreate(BaseModel):
    
    name: str = Field(..., min_length=2)
    description: str | None = None
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=1)

    # def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
        
        
        
