from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, status
from requests import get 
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
    
class ProductModel(BaseModel):
    id: int
    title: str
    slug: str
    price: float
    description: str
    images: List[str]
    class Config:
        extra = "ignore"

BASE_URL = 'https://api.escuelajs.co/api/v1'
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    # Default port when running angular
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"Hello": "This is the api for the Test in the Creative Innovation Company. To get the products use /products "}


@app.get("/products/", status_code=status.HTTP_200_OK)
async def get_products(db: db_dependency):
    
    #** Load all products from the api to the db
    # products = get(f"{BASE_URL}/products")
    # for p in products.json():
    #     product_clean = ProductModel(**p)
    #     db_product = models.Product(**product_clean.dict())
    #     db.add(db_product)
    #     db.commit()

    products = db.query(models.Product).all()
    return products


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: db_dependency, q: Union[str, None] = None):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, db: db_dependency):
    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
    except:
        raise HTTPException(409, 'Error creating the product')


@app.patch("/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_update: dict, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    for key, value in product_update.items():
        if hasattr(product, key):
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, detail='Product not found')
    db.delete(product)
    db.commit()