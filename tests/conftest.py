from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app import schemas, models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from alembic import command
from app.oauth2 import create_access_token

# https://youtu.be/0sOvCWFmrtA?t=58751

# special test that pytest uses to define fixtures for any test within the tests package, including subpackages

# conftest.py can be scoped to a package and inherited to certain tests but not others, i.e. if we had an API package we could have a conftest within it too

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

@pytest.fixture
def create_test_user(client):
    # need to call create user route, so need client
    user_data = {"email": "fixture_test_user@gmail.com", "password":"password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    user = res.json()
    user['password'] = user_data['password']
    return user

@pytest.fixture
def create_test_second_user(client):
    # need to call create user route, so need client
    user_data = {"email": "fixture_test_user_2@gmail.com", "password":"password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    user = res.json()
    user['password'] = user_data['password']
    return user

# for oauth2 testing
@pytest.fixture
def token(create_test_user):
    # import create_access_token() from oauth2.py
    # create access token takes in a dict containing user_id
    return create_access_token({"user_id": create_test_user['id']})

# for clients that require authorization
@pytest.fixture
def authorized_client(client, token):
    # update the headers to contain the token, add the Authorization header with Bearer {token} as the content
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# create test posts for testing the post and vote functionality
@pytest.fixture
def create_test_posts(create_test_user, create_test_second_user, session):
    post_data = [{
        "title": "first post",
        "content": "first content",
        "user_id": create_test_user['id']
    },
    {
        "title": "second post",
        "content": "second content",
        "user_id": create_test_user['id']
    },
    {
        "title": "third post",
        "content": "third content",
        "user_id": create_test_second_user['id']
    }]
    # create 3 posts using SQLAlchemy - session.add_all
    # session.add_all([models.Post(title='x', content='y', user_id='z')])
    # session.commit()
    # session.query(models.Post).all()

    # However, to not hard code it use the map function
    # map(func, posts_data), where the function iterates over the list and converts to models.Post
    def create_post_model(post):
        # convert a dictionary to a post
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    # returns a map, but not a list
    post_list = list(post_map)
    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
