from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from requests import get 
from fastapi.middleware.cors import CORSMiddleware

class Category(BaseModel):
    id: int
    name: str
    slug: str
    image: str
    
class Product(BaseModel):
    id: int
    title: str
    slug: str
    price: float
    description: str
    category: Category

app = FastAPI()

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

baseUrl = 'https://api.escuelajs.co/api/v1'

@app.get("/")
def read_root():
    return {"Hello": "This is the api for the Test in the Creative Innovation Company. To get the products use /products "}

@app.get("/products/")
def get_products():
    products = get(f"{baseUrl}/products")
    return products.json()

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, q: Union[str, None] = None):
    product = get(f"{baseUrl}/product/{product_id}")
    return product.json()