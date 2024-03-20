from sqlalchemy import Boolean, Integer, String,Text, ForeignKey, Column
from core.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer,primary_key=True)
    username =Column(String,default=True)
    email = Column(String,unique=True,nullable=False)
    password = Column(Text,nullable=True)
    cart=relationship('Cart', back_populates='user')



class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    categor_Name= Column(String, index=True)
    product=relationship('Product', back_populates='category')

    
class Product(Base):
    __tablename__="product"

    id= Column(Integer, primary_key=True, index=True)
    name=Column(String,index=True)
    description = Column(String,default=False)
    price = Column(Integer,default=False)
    freshness=Column(String, default=False)
    Stock = Column(String, default=False)
    review = Column(String, default=False)
    categor_id=Column(Integer,ForeignKey('category.id'))
    category=relationship('Category', back_populates='product')
    cart=relationship('Cart', back_populates='product')



class Profile(Base):
    __tablename__ ="profile"

    id = Column(Integer,primary_key=True)
    frist_name = Column(String,default=False)
    last_name = Column(String,default=False)
    email = Column(String,index=True)
    phone_number=Column(Integer,default=False)
    address= Column(String,default=False)
    City = Column(String,default=False)
    state = Column(String,default=False)
    pin_code = Column(Integer,default=False)



class Cart(Base):
    __tablename__= "cart"

    id = Column(Integer,primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    user_id =Column(ForeignKey('user.id'))
    user = relationship("User",back_populates="cart")
    product= relationship("Product", back_populates='cart')



# class Order(Base):
#     ORDER_STATUS=(
#         ('PENDING','pending'),
#         ('IN-TRANSIT','in_transit'),
#         ('DELIVERRED','delivered')
#     )
#     __tablename__="orders"
#     id =  Column(Integer,primary_key=True)
#     quantity = Column(Integer,nullable=False)
#     order_status=Column(ChoiceType(Choice=ORDER_STATUS),default="PENDING")
#     user_id= Column(Integer,ForeignKey('user.id'))
#     user=relationship("User",back_populates='orders')

