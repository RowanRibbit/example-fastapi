from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from alembic import command

# using our development or production DB for testing; when we import our client using our fastapi_db, but want a completely separate DB. Go to database.py and see that session is passed into our routers


# for testing, can hardcode the URL
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to DB need a session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# how do we override the DB? FastAPI Docks > Overrides, app.dependency.override and testing a database


# swaps the dependencies out for testing

# can make a fixture dependent on another fixture
@pytest.fixture(scope='function')
def session(): 
    # use SQLAlchemy to build the DB
    # run our code before we run our test, drop the tables then create the tables

    # alembic
    # command.upgrade('head')    
    # command.downgrade('base')

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # will yield the db to the client fn()
    try:
        yield db
    finally:
        db.close()
# by making session a fixture, can also pass it as a fixture to test fns to perform session.query(x) on db object

# fixture (dependent fixtures must have same scope)
@pytest.fixture(scope='function')
def client(session):
    # dependent on session, so performs the session fn()
    def override_get_db():
        try:
            yield session
        finally:
            session.close()    
    
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # now can pass client through as a fixture in our tests, so can change it a little, yield behaves like return

    # run our code after our test finishes