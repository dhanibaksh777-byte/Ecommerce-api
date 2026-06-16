from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from database import get_db
from utlis.email import send_email
from Routers.auth import verify_token
from errors import NotFoundException, UnauthorizedException, AlreadyExistsException
from fastapi import BackgroundTasks
import schemas
import models


router = APIRouter()


@router.post("/create-order")
def create_order(order: schemas.CreateOrder, background_task : BackgroundTasks ,user_id=Depends(verify_token), db: Session = Depends(get_db)):
    new_order = models.order(user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product_id in order.product_id:
        order_product = models.order_products(order_id=new_order.id, product_id=product_id)
        db.add(order_product)

    db.commit()
    background_task.add_task(send_email, "user@gmail.com", "Order Placed", "your order has been placed!")
    return new_order

@router.get("/my-orders/{order_id}")
def get_order(order_id : int , user_id = Depends(verify_token), db : Session = Depends(get_db)):
    order = db.query(models.order).filter(models.order.id == order_id,models.order.user_id==user_id).first()
    if not order:
        raise NotFoundException("order not found!")
    
    return order

@router.get("/my-orders")
def get_notes(page : int = 1 , limit : int = 2, _=Depends(verify_token) ,db : Session = Depends(get_db)):
    skip = (page -1) * limit
    order = db.query(models.order).offset(skip).limit(limit).all()
    return order


@router.delete("/delete-order/{order_id}")
def delete_order(order_id : int ,user_id = Depends(verify_token), db : Session = Depends(get_db)):
    order = db.query(models.order).filter(models.order.id == order_id , models.order.user_id == user_id).first()
    if not order:
        raise NotFoundException("order not found!")
    db.delete(order)
    db.commit()
    return {"order deleted!"}