from fastapi import FastAPI,Depends,HTTPException,Query,APIRouter
import users.models as models
from core.database import engine
from users.routers import user_router, router as guest_router
from auth.route import auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth

from core.database import sessionLocal
from typing import List
from sqlalchemy.orm import Session
from users.models import Category,Product
from core.database import Base,get_db
from users.schema import ItemCreate,ProductCreate,UpdateProduct


Product_router= APIRouter(
     prefix='/products',
     tags=['Products']
)

# From Here we will create CRUD operations for Products

# ADD Product in Database


@Product_router.post("/product/items/")
def create_item(item: ProductCreate,db: Session = Depends(get_db)):
    db_item = Product(
        id=item.id,
        name=item.name.title(),
        description=item.description.title(),
        price=item.price,
        freshness=item.freshness.title(),
        Stock=item.Stock.title(),
        review=item.review,
        categor_id=item.categor_id
    )
    already_exit=db.query(Product).filter(Product.id == item.id).first()
    if already_exit is not None:
        raise HTTPException(status_code=404,detail="This Product Alredy Exits ")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"Message":'Product Added Successfully'}

# Read all the Products from the Database


@Product_router.get("/products/data/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get 1 Data from Product database


@Product_router.get("/product/{product_id}")
def read_item(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update Product in Database
@Product_router.put("/update/{product_id)")
def update_item(item_id:int, product_update: UpdateProduct, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in product_update.dict().items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return {"Message":"Product Updated successfully"}

# Delete Product by Product_id


@Product_router.delete("/Product/{product_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

# search product by product name


@Product_router.get("/products/")
async def search_products(query: str = Query(None, min_length=1), db: Session = Depends(get_db)):
    results = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
    if not results:
        raise HTTPException(status_code=404,detail="Product not Found ")
    return results


# get products by Category
@Product_router.get("/categories/{category_id}/product")
async def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.product

