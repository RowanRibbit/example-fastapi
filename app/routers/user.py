from .. import schemas, models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

# router instead of app
router = APIRouter(
    prefix='/users',
    tags = ['Users']
)

# User functions
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    # hash the password
    hash_pw = utils.hash(user.password)
    user.password = hash_pw

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def get_user(id: int, db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Error - User with id: {id} Not Found")
    return user

@router.get('/', response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    user = db.query(models.User).all()    

    return user

@router.put('/{id}', response_model=schemas.UserResponse)
async def update_user(id: int, user: schemas.UserUpdate, db: Session=Depends(get_db)):
    updated = db.query(models.User).filter(models.User.id == id)

    if not updated.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Error - User with id: {id} Not Found")
    
    updated.update(user.dict(), synchronize_session=False)
    db.commit()

    return updated.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int,db: Session=Depends(get_db)):
    
    deleted = db.query(models.User).filter(models.User.id == id)

    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Error - User with id: {id} Not Found')
    
    deleted.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)