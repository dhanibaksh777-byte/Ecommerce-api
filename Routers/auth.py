from fastapi import APIRouter,Depends,HTTPException
from errors import NotFoundException, UnauthorizedException, AlreadyExistsException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from datetime import datetime,timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import models
import bcrypt
import schemas
import os


oauth_scheme2 = OAuth2PasswordBearer(tokenUrl="Login")
load_dotenv()

secrete_key = os.getenv("secrete_key")
access_token_expire = int(os.getenv("access_token_expire"))
algorithim = "HS256"



def hash_password(password : str):
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

def create_token(data : dict):
    Expire = datetime.utcnow() + timedelta(minutes=access_token_expire)
    data["exp"] = Expire
    token = jwt.encode(data,secrete_key,algorithm=algorithim)
    return token

def verify_token(token : str = Depends(oauth_scheme2)):
    try:
        payload = jwt.decode(token ,secrete_key,algorithms=[algorithim])

        user_id = payload.get("user_id")

        if not user_id:
            raise UnauthorizedException("invalid token")
        
    except JWTError:
        raise UnauthorizedException("invalid token")
    
    return user_id 


router = APIRouter()


@router.post("/Register",response_model=schemas.UserResponse)
def Register(user : schemas.CreateUser,db : Session = Depends(get_db)):
    existing_email = db.query(models.user).filter(models.user.email == user.email).first()
    if existing_email:
        raise AlreadyExistsException("email already exists")

    existing_username = db.query(models.user).filter(models.user.username == user.username).first()
    if existing_username:
        raise AlreadyExistsException("username already exists")
    
    hashed_password = hash_password(user.password)
    new_user = models.user(email = user.email , username = user.username,password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/Login")
def Login(user : schemas.LoginUser,db : Session = Depends(get_db)):
    db_user = db.query(models.user).filter( models.user.email == user.email).first()
    if not db_user:
        raise NotFoundException("user not found!")
    password_check = bcrypt.checkpw(user.password.encode("utf-8"),db_user.password.encode("utf-8"))
    if not password_check:
        raise UnauthorizedException("incorrect password!")
    token = create_token({"user_id":db_user.id})
    return {"token": token, "token_type": "bearer"}

