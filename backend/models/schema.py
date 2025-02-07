from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    contact_info = Column(String(255))
    location = Column(String(255))

    # Establishing the relationship with Product
    products = relationship("Product", back_populates="supplier", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, index=True)

    # Establishing the reverse relationship with Supplier
    supplier = relationship("Supplier", back_populates="products")
