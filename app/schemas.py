from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
from pydantic.types import conint


# user Schema, moved to top so it can be seen by PostResponse so the UserResponse can be added to the pydantic model
class UserBase(BaseModel):
    email: EmailStr
    # hash the password - FastAPI Security > Oauth2 with Password
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Pydantic/Schema model for Post, defines structure of a request+response, ensures that reuqest will only go through with content, provides validation of the body field
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value
    rating: Optional[int] = None # Optional var

# specific method models inherit from base class
class PostCreate(PostBase):
    pass

class PostUpdatePublished(PostBase):
    published: bool

class PostUpdate(PostBase):
    pass

# define a pydantic schema model for returned data, i.e., don't want to return certain fields or properties
class PostResponse(PostBase):
    created_at: datetime
    id: int
    user_id: int
    user: UserResponse
    # need to convert SqlAlchemy model to Python Dict
    class Config: 
        orm_mode = True

class PostVote(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True

# define a schema for the access_token and token_type
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# vote schema
class VoteBase(BaseModel):
    post_id: int
    # direction less than or equal to 1
    dir: conint(le=1)