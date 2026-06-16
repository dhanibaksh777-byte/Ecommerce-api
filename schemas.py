from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import List

class CreateUser(BaseModel):
    username : str 
    email : EmailStr
    password : str 

class UserResponse(BaseModel):
    id : int 
    username : str 

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    email : EmailStr
    password : str 


class CreateOrder(BaseModel):
    product_id : list[int]


class OrderResponse(BaseModel):
    id : int 
    status : str 
    created_at : datetime
    
    class Config:
        from_attributes = True


class CreateProduct(BaseModel):
    name : str
    price : int

class productResponse(BaseModel):
    id : int 
    name : str
    price : int


    class Config:
        from_attributes = True












