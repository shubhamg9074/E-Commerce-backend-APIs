
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from passlib.context import  CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from core.database import get_db
from core.config import get_settings
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi import Depends
from users.models import User
settings=get_settings()

pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_schema =OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_pass_hash(password):
    return pwd_context.hash(password)

def verify_password(pain_password, hashed_password):
    return pwd_context.verify(pain_password,hashed_password)

async def create_access_token(data, expiry:timedelta):
    payload=data.copy()
    expiry_in =datetime.utcnow() + expiry
    payload.update({"exp": expiry_in})
    token= jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    return token

async def create_refresh_token(data):
    return jwt.encode(data,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token):
    try:
        payload= jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        return None
    return payload


def get_current_user(token: str = Depends(oauth2_schema), db = None):
    payload =  get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None
    user_id = payload.get('id', None)
    if not user_id:
        return None
    if not db:
        db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    return user



class JWTAuth:
    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()   
        if 'authorization' not in conn.headers:
            return guest 
        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest
        user = get_current_user(token=token)
        
        if not user:
            return guest
        return AuthCredentials('authenticated'), user
