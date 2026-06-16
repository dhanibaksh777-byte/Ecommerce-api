from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from datetime import datetime
from database import base
from sqlalchemy.orm import Relationship


class user(base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(200),unique=True)
    email = Column(String(200),unique=True)
    password = Column(String(200))

    order = Relationship("order",back_populates="owner")

class order(base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.utcnow)
    status = Column(String(200),default="pending")
    user_id = Column(Integer,ForeignKey("users.id"))
    owner = Relationship("user",back_populates="order")


class product(base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(200))
    price = Column(Integer)

    

class order_products(base):
    __tablename__ = "order_products"
    id = Column(Integer,primary_key=True,index=True)
    order_id = Column(Integer,ForeignKey("orders.id"))
    product_id = Column(Integer,ForeignKey("products.id"))


