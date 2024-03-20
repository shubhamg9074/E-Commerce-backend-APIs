


from fastapi import FastAPI,Depends,HTTPException,Query
import users.models as models
from core.database import engine
from users.routers import user_router, router as guest_router
from auth.route import auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth
from admin.category import Category_router
from admin.products import Product_router


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(Category_router)
app.include_router(Product_router)

# add  middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
async def hello():
    return {"message":"Hello World"}


'''
@app.post("/Catogery/items/")
def create_item(item: ItemCreate,db: Session = Depends(get_db)):
    db_item = Category(id=item.id,categor_Name=item.categor_Name.title())
    already_exit=db.query(Category).filter(Category.id == item.id).first()
    if already_exit is not None:
        raise HTTPException(status_code=404, detail="This Category alredy Exits")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"Message":"Catogery Addded successfully"}


# Get all items
@app.get("/Catogery/data/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Get a single item by ID
@app.get("/Catogery/{catogery_id}")
def read_item(catogery_id: int, db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == catogery_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update an item by ID
@app.put("/Update_Cat/{item_id}")
def update_item(item_id: int, categor_Name: str, db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    #Category.id = id
    Category.categor_Name = categor_Name
    db.commit()
    return {"message": "Item updated successfully"}

# Delete an item by ID
@app.delete("/Delete_Cat/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
'''

""""
# From Here we will create CRUD operations for Products

# ADD Product in Database
@app.post("/product/items/")
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
@app.get("/products/data/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get 1 Data from Product database
@app.get("/product/{product_id}")
def read_item(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update Product in Database
@app.put("/update/{product_id)")
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
@app.delete("/Product/{product_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

#search product by product name
@app.get("/products/")
async def search_products(query: str = Query(None, min_length=1), db: Session = Depends(get_db)):
    results = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
    if not results:
        raise HTTPException(status_code=404,detail="Product not Found ")
    return results


# get products by Category
@app.get("/categories/{category_id}/product")
async def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.product

"""




