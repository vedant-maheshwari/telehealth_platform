from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, database

app = FastAPI()

models.Base.metadata.create_all(bind = database.engine)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_db():
    db = database.session_local()
    try:
        yield db

    finally:
        db.close()

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    role: str = "patient"


@app.get('/')
def home():
    return {"message": "Welcome to Telehealth Project!"}

@app.post('/register')
def register(user : RegisterUser, db: Session = Depends(get_db)):
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_pw, role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "email": db_user.email, "role": db_user.role} 
