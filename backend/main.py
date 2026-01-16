from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.databases import SessionLocal, engine
from database import databasemodels
from database.models_db import (
    ProductCreate,
    ProductUpdate,
    UserCreate,
    UserLogin,
)
app = FastAPI(title="JustKart API")

# create tables
databasemodels.Base.metadata.create_all(bind=engine)


# ---------------- DB Dependency ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Password Helpers ----------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


# ---------------- Auth APIs ----------------

from fastapi import HTTPException

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(databasemodels.User)\
            .filter(databasemodels.User.username == user.username).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        new_user = databasemodels.User(
            username=user.username,
            hashed_password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        # 👇 CRITICAL: always return JSON
        raise HTTPException(
            status_code=500,
            detail="Registration failed due to server error"
        )

@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        existing = db.query(databasemodels.User)\
            .filter(databasemodels.User.username == user.username).first()

        if not existing or not verify_password(user.password, existing.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "message": "Login successful",
            "user_id": existing.id,
            "username": existing.username
        }

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Login failed due to server error"
        )

# ---------------- Product APIs ----------------

@app.get("/products/{user_id}")
def get_products(user_id: int, db: Session = Depends(get_db)):
    return db.query(databasemodels.Product)\
        .filter(databasemodels.Product.user_id == user_id)\
        .all()


@app.post("/add_product")
def add_product(
    product: ProductCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    new_product = databasemodels.Product(
        **product.model_dump(),
        user_id=user_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/edit_product/{pid}")
def update_product(pid: int, product: ProductUpdate, db: Session = Depends(get_db)):
    existing = db.query(databasemodels.Product)\
        .filter(databasemodels.Product.id == pid).first()

    if not existing:
        return {"error": "product not found"}

    if product.name is not None:
        existing.name = product.name
    if product.description is not None:
        existing.description = product.description
    if product.price is not None:
        existing.price = product.price
    if product.quantity is not None:
        existing.quantity = product.quantity

    db.commit()
    return {"message": "product updated successfully"}


@app.delete("/delete/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db)):
    product = db.query(databasemodels.Product)\
        .filter(databasemodels.Product.id == pid).first()

    if not product:
        return {"error": "product not found"}

    db.delete(product)
    db.commit()
    return {"message": "product deleted successfully"}
