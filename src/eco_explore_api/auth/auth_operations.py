from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
import eco_explore_api.auth.auth_database as au_db
import eco_explore_api.config as cf
import eco_explore_api.constants.response_constants as rcodes
import eco_explore_api.auth.models as auth_models
import eco_explore_api.auth.auth_database as auth_database
import eco_explore_api.auth.auth_operations as auth_operations

SECRET_KEY = cf.SECRET_KEY_AUTH
ALGORITHM = cf.AUTH_ALGORITH
ACCESS_TOKEN_EXPIRE_MINUTES = 86400

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=rcodes.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, cf.SECRET_KEY_AUTH, algorithms=[cf.AUTH_ALGORITH])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = auth_database.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def check_if_user_is_auth(user_id, token):
    try:
        user = await get_current_user(token)
        return user.id == user_id
    except Exception:
        return False


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = au_db.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.Clave):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
