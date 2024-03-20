from fastapi import APIRouter,Depends,status,Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from auth.services import get_token
from auth.services import get_refresh_token
auth_router =APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post("/token",status_code=status.HTTP_200_OK)
async def authenticate_user(data:OAuth2PasswordRequestForm =Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)

@auth_router.post("/refresh",status_code=status.HTTP_200_OK)
async def refresh_access_token (refersh_token: str = Header(),db:Session = Depends(get_db)):
    return await get_refresh_token(token=refersh_token,db=db)
