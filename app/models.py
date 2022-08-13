# file for DB Table Models
from typing import Text
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
# migration manager - alembic (all track changes to database schema and rollback changes), can automatically pull DB models from SqlAlchemy to generate the proper tables
# alembic init [dirname], makes file and alembic.ini
# go to .env, make sure it can access Base

# Will use the app to create the tables later
# SQLAlchemy Model for defining columns of our tables within postgres; used to query, create, delete and update entries in DB
class Post(Base):
    # what do we want to call this table in Postgres
    __tablename__ = 'posts'
    # define the table columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    rating = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # use SQLAlchemy to make the foreign key to the table name
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = relationship('User')

class User(Base):
    __tablename__ = 'user'
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=Text('NOW()'))
    phone_number = Column(String, nullable=True)

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False, primary_key=True)
