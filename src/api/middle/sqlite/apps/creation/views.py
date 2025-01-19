from loguru import logger
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Type

import sqlite3
import os
from apps.creation import models

router = APIRouter(
    prefix="/creation"
)

@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
# Pydantic models for request and response schemas
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    name: str
    description: str

class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str
    email: str

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crud_operations(model: Type[models.Base], db: Session):
    def create_item(db: Session, item: model):
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_items(db: Session, skip: int = 0, limit: int = 10):
        return db.query(model).offset(skip).limit(limit).all()

    def get_item(db: Session, item_id: int):
        return db.query(model).filter(model.id == item_id).first()

    def update_item(db: Session, item_id: int, item: model):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.__dict__.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    def delete_item(db: Session, item_id: int):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"detail": "Item deleted successfully"}

    return {
        "create": create_item,
        "read_all": get_items,
        "read_one": get_item,
        "update": update_item,
        "delete": delete_item,
    }

@router.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud_operations(models.Item, db)["create"](db, models.Item(**item.dict()))

@router.get("/items/", response_model=List[ItemCreate])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_operations(models.Item, db)["read_all"](db, skip, limit)

@router.get("/items/{item_id}", response_model=ItemCreate)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud_operations(models.Item, db)["read_one"](db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=ItemCreate)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    return crud_operations(models.Item, db)["update"](db, item_id, models.Item(**item.dict()))

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud_operations(models.Item, db)["delete"](db, item_id)

@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_operations(models.User, db)["create"](db, models.User(**user.dict()))

@router.get("/users/", response_model=List[UserCreate])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_operations(models.User, db)["read_all"](db, skip, limit)

@router.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_operations(models.User, db)["read_one"](db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserCreate)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return crud_operations(models.User, db)["update"](db, user_id, models.User(**user.dict()))

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud_operations(models.User, db)["delete"](db, user_id)