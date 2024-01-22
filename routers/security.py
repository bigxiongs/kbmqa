from datetime import timedelta, datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt

from ogm import *

SECRET_KEY = "1626204a656f593083bd1de20b7eab415217243a89ee4c06be0fd74ec8f49a6c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Wrong arguments",
    headers={"WWW-authenticate": "Bearer"},
)
service_unavailable_exception = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service unavailable",
)


def hash_password(password: str) -> str:
    """Password hash function"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Check whether a password is valid."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> User:
    """Check whether a user is valid: it's in the database, and it's password is correct."""
    user = User(models.UserBase(username))
    if not user.exists():
        raise forbidden_exception
    try:
        if verify_password(password, user.password):
            return user
    except Exception:
        raise credentials_exception


def authenticate_application_form(form_data: OAuth2PasswordRequestForm) -> User:
    """Dependence to verify an application from."""
    return authenticate_user(form_data.username, form_data.password)


def create_access_token(username) -> str:
    """Create a access token from data and an expire delta.
    data { "sub": username }
    """
    data = {"sub": username}
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Get current user from an access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub", None)
        user = User(models.UserBase(username))
    except JWTError:
        raise credentials_exception
    if not user.exists():
        raise forbidden_exception
    return user


def create_user(username: str, password: str, telephone: str = "", email: str = "", profile: str = ""):
    """Create a new user"""
    if User(models.UserBase(username)).exists():
        raise forbidden_exception
    user = models.User(username, hash_password(password), telephone, email, profile, datetime.now())
    if User(user).exists():
        return User(models.UserBase(username))
    raise service_unavailable_exception


def get_current_dialogue(did: int, current_user: Annotated[User, Depends(get_current_user)]):
    dialogue = current_user.get_dialogue(did)
    if dialogue is None:
        raise forbidden_exception
    return dialogue


def get_current_graph(gid: int, current_user: Annotated[User, Depends(get_current_user)]):
    graph = current_user.get_graph(gid)
    if graph is None:
        raise forbidden_exception
    return graph


def create_node(labels: list[str], properties: dict[str, Any]):
    return models.KNode(labels, properties)


def create_edge(k_type: str, properties: dict[str, Any], start_node: int, end_node: int):
    return models.KRelationship(k_type, properties, start_node, end_node)
