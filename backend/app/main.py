from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import SessionLocal, engine, Base
from models.schema import Product, Supplier
from pydantic import BaseModel
from typing import List
from transformers import pipeline
from rapidfuzz import process, fuzz

app = FastAPI()

# Initialize GPT model for chatbot response
chatbot = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Welcome to Chatbot AI API"}

# Pydantic response models
class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: str
    location: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    supplier_id: int

    class Config:
        from_attributes = True

# Get all suppliers
@app.get("/suppliers/", response_model=List[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

# Get all products
@app.get("/products/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Pydantic models for request validation
class SupplierCreate(BaseModel):
    name: str
    contact_info: str
    location: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    supplier_id: int

# Create a new supplier
@app.post("/suppliers/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    new_supplier = Supplier(**supplier.dict())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

# Create a new product
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Pydantic model for chatbot query
class QueryRequest(BaseModel):
    query: str

@app.post("/chatbot/")
def chatbot_response(query: QueryRequest, db: Session = Depends(get_db)):
    query_text = query.query.lower()

    # Get all product and supplier names
    product_names = [product.name for product in db.query(Product).all()]
    supplier_names = [supplier.name for supplier in db.query(Supplier).all()]

    # Find closest match using fuzzy search
    best_product_match = process.extractOne(query_text, product_names, scorer=fuzz.ratio) if product_names else None
    best_supplier_match = process.extractOne(query_text, supplier_names, scorer=fuzz.ratio) if supplier_names else None

    # Extract values safely
    if best_product_match:
        best_product, product_score, _ = best_product_match  # Ignore the third value
    else:
        best_product, product_score = None, 0

    if best_supplier_match:
        best_supplier, supplier_score, _ = best_supplier_match  # Ignore the third value
    else:
        best_supplier, supplier_score = None, 0

    # Set a threshold for a match
    threshold = 70  

    if best_product and product_score >= threshold:
        product = db.query(Product).filter(Product.name == best_product).first()
        if product:
            return {"response": f"Product Found: {product.name}, Price: {product.price}"}

    if best_supplier and supplier_score >= threshold:
        supplier = db.query(Supplier).filter(Supplier.name == best_supplier).first()
        if supplier:
            return {"response": f"Supplier Found: {supplier.name}, Location: {supplier.location}"}

    return {"response": "No relevant product or supplier found. Please refine your query."}
