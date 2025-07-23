from random import random
from passlib.context import CryptContext
from names_generator import generate_name
from . import models
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_username(db: Session) -> str:
    while True:
        username = generate_name(style='underscore').lower()

        username = f"{username}_{random.randint(10, 99)}"

        existing_user = db.query(models.User).filter(models.User.username == username).first()
        if not existing_user:
            return username

def is_username_taken(db: Session, username: str) -> bool:
    return db.query(models.User).filter(models.User.username == username).first() is not None

        
