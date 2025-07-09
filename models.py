from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), unique=True)
    slug = Column(String(20))
    price = Column(Float)
    description = Column(String(500))
    images = Column(JSON)