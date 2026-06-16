from fastapi import APIRouter,Depends
from utlis.email import send_email
from fastapi import BackgroundTasks
from database import get_db
from Routers.auth import verify_token
from errors import NotFoundException, UnauthorizedException, AlreadyExistsException
from sqlalchemy.orm import Session 
import models 
import schemas


router = APIRouter()

@router.post("/create-product")
def create_product(product : schemas.CreateProduct, background_tasks : BackgroundTasks, _=Depends(verify_token),  db : Session = Depends(get_db)):
    new_product = models.product(name = product.name , price = product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)


    background_tasks.add_task(send_email, "admin@gmail.com", "New Product", f"{new_product.name} created!")
    return new_product


@router.get("/get-product")
def get_products(page : int = 1, limit : int = 2,db : Session = Depends(get_db)):
    skip = (page - 1) * limit
    products = db.query(models.product).offset(skip).limit(limit).all()
    return products


@router.get("/get-product/{product_id}")
def get_product(product_id : int , db : Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id == product_id).first()
    if not product:
        raise NotFoundException("product not found!")
    
    return product

@router.put("/update-product/{product_id}")
def update_product(product_id : int ,new_name : str , new_price : int , updated : schemas.CreateProduct, _=Depends(verify_token), db : Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id == product_id).first()
    if not product:
        raise NotFoundException("product not found!")
    product.name = updated.name
    product.price = updated.price
    db.commit()
    db.refresh(product)
    return {"product updated!"}



@router.delete("/delete-product/{product_id}")
def delete_product(product_id: int, _=Depends(verify_token), db: Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id == product_id).first()
    if not product:
        raise NotFoundException("product not found!")
    
    db.query(models.order_products).filter(models.order_products.product_id == product_id).delete()
    
    db.delete(product)
    db.commit()
    return {"product deleted!"}
    
    