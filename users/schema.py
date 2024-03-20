from pydantic import BaseModel
from typing import Optional

class SignUpModal(BaseModel):
    id : Optional[int]
    username :str
    email : str
    password : str

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token:str
    refresh_token:str
    token_typ:str = "Bearer"
    expires_in:int

    
class LoginModel(BaseModel):
    id:Optional[int]
    email:str
    password:str

    class Config:
        orm_mode=True


class ItemCreate(BaseModel):
    id: int
    categor_Name: str


class ProductCreate(BaseModel):
    id:int
    name:str
    description:str
    price:int
    freshness:str
    Stock:str
    review:str
    categor_id:int

class UpdateProduct(BaseModel):
    name:str
    description:str
    price:int
    freshness:str
    Stock:str
    review:str
    categor_id:int

