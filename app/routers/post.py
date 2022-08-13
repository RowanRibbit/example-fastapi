from .. import schemas, models, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db

# video https://youtu.be/0sOvCWFmrtA?t=30719

# router
router = APIRouter(
    prefix='/posts',
    tags = ['Posts'] # for the swagger API docs
)

# define the query params
@router.get('/', response_model=List[schemas.PostVote])
def get_posts(db: Session=Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # when you use sqlalchemy in FastAPI, call the session
    # get the user's posts

    # limit and skip are query params, how to do pagination
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).all()    
    # Query command just performs a SQL Query under the hood
    # apply joins in SQLAlchemy, join on the votes table, by default is left inner join but in postgres is left outer
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # will error due to pydantic validation

    return results


# @app.get("/posts")
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     # print(posts)
#     return {'data': posts}

# add Oauth2 dependency
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(new_post: schemas.PostCreate, db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # Do this way to prevent SQL Injection, sanitises input
    # Stage the changes
    # cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published, new_post.rating))
    # post = cursor.fetchone()
    # Commit the post
    # connection.commit()


    # manually mapping kwargs
    # post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published, rating=new_post.rating)

    # post is a dict, so unpack the dict

    # test Oauth

    post = models.Post(**new_post.dict(), user_id = current_user.id)

    # SQLalchemy doesn't have the return * thing, so use db.refresh(post)
    db.add(post)
    db.commit()
    db.refresh(post)

    # for response_model need to add class Config orm_mode=True

    return post


# validate the data: title str, content str

@router.get('/{id}', response_model=schemas.PostVote)
async def get_post(id: int,db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): 
    # cursor.execute("""SELECT * FROM posts where id = %s """, (id,))
    # post = cursor.fetchone()
    
    print(current_user.email)
    # user filter to query, and use first to get first result
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Error - Post with id: {id} Not Found")
    return post

@router.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostUpdate, db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" Update posts set title = %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content, post.published, id))
    
    # updated = cursor.fetchone()

    # connection.commit()
    
    print(current_user.id)
    updated = db.query(models.Post).filter(models.Post.id == id)

    if not updated.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Error - Post with id: {id} Not Found")
    
    if current_user.id != updated.first().user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorised to perform requested action')

    updated.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return updated.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    
    print(current_user)
    # cursor.execute(""" DELETE FROM posts where id = %s returning * """, (str(id),))
    # deleted = cursor.fetchone()
    # connection.commit()
    deleted = db.query(models.Post).filter(models.Post.id == id)

    post = deleted.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Error - Post with id: {id} Not Found')
    print(post.user_id)
    print(current_user.id)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorised to perform requested action')
    
    deleted.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
