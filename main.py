from fastapi import FastAPI
from database import engine
from Routers import products
from Routers import orders
from Routers import auth
import models
from fastapi.middleware.cors import CORSMiddleware
models.base.metadata.create_all(bind=engine)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(orders.router, prefix="/orders")

