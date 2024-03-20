from fastapi import FastAPI,Depends,HTTPException,Query,APIRouter
import users.models as models
from core.database import engine
from users.routers import user_router, router as guest_router
from auth.route import auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth


from sqlalchemy.orm import Session
from users.models import Category,Product
from core.database  import Base,get_db
from users.schema import ItemCreate,ProductCreate,UpdateProduct


Category_router= APIRouter(
     prefix='/category',
     tags=['Category']
)


@Category_router.post("/Catogery/items/")
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
@Category_router.get("/Catogery/data/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Get a single item by ID


@Category_router.get("/Catogery/{catogery_id}")
def read_item(catogery_id: int, db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == catogery_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update an item by ID
@Category_router.put("/Update_Cat/{item_id}")
def update_item(item_id: int,item_update:ItemCreate,db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.id = item_update.name
    item.categor_Name = item_update.categor_Name
    db.commit()
    return {"message": "Item updated successfully"}

# Delete an item by ID


@Category_router.delete("/Delete_Cat/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Category).filter(Category.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
