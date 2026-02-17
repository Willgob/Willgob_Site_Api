from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, utils
from database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email exists
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = utils.hash_password(user.password)

    # Create user object
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw
    )

    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
