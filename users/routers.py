from fastapi import APIRouter, Request
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from core.database import sessionLocal,engine
from users.models import User
from users.schema import SignUpModal
from fastapi.responses import JSONResponse
from core.database import get_db
from core.security import get_pass_hash
from core.security import oauth2_schema, get_current_user
from users.schema import LoginModel


router =APIRouter(
     prefix='/users',
     tags=['User']
)

user_router =APIRouter(
     prefix='/users',
     tags=['User'],
     dependencies=[Depends(oauth2_schema)]
)

session=sessionLocal(bind=engine)


@router.post('/signup',
                  status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpModal, db: Session=Depends(get_db)):
    db_email= session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the email already exists")
    new_user=User(
        username=user.username,
        email=user.email,
        password=get_pass_hash(user.password)
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    payload={"message":"User account has beed succesfully created."}
    return JSONResponse(content=payload)

@user_router.post("/me",status_code=status.HTTP_200_OK,response_model=SignUpModal)
async def get_user_Details(request:Request):
    return request.user