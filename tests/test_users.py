from app import schemas
from app.config import settings
from jose import jwt
import pytest

# https://youtu.be/0sOvCWFmrtA?t=54591

# pytest /users and /users/ are actually a little different
# /users does a HTTP 307 Temporary Redirect, but can be an issue in testing as res.status_code will see 307 first

def test_get_users(client):
    res = client.get('/users/')
    # response object
    # what's the payload: x.json()
    # assert res.json().get('id') == 1
    assert res.status_code == 200

# other pytest flags we can pass
# depending on packages and libraries
# pytest --disable-warnings removes the excess warnings
# default behaviour is when a test fails, keeps doing other tests
# to turn this off run pytest --disable-warnings -v -x, when the first test fails exits running tests



# Simulate testing a user
def test_create_user(client):
    # pass json in the body, as a python dictionary, in the case as the UserCreate schema
    res = client.post('/users/', json={"email": "email_test_create@email.com", "password": "password123"})
    print(res.json())
    # unpack the res.json() dictionary, automatically checks for the properties of UserResponse
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "email_test_create@email.com"
    assert res.status_code == 201

# run multiple tests - will still get duplicate key violation: make use of fixtures
# fixtures have a specific scope, have the default function scope (run before each dependent fn), so db is dropped between creation and login
# pytest examples to explain the scopes of fixtures, search for scope
# default is function, but has others like class, module, package, session
# class for a specific class, module is all the tests in a module, packages and session runs once at the start of the test session and destroyed at the end
# go back to tests/database.py

# not a good test as is dependent on another test, how do we make login test case independent of test_create_user()
# create a fixture for creating a user (move all fixtures to conftest.py)

def test_login_user(client, create_test_user):
    # don't need trailing slash for login based on our auth router
    res = client.post('/login', data={"username": create_test_user['email'], "password": create_test_user['password']})
    # assert the token is valid
    login_response = schemas.Token(**res.json())
    # validate the token - decode the token like we do in oauth2 file
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == create_test_user['id']
    assert login_response.token_type == 'bearer'    
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('fixture_test_user@gmail.com', 'wrongpass', 403),
    ('wrong@email.com', 'wrongpass', 403),
    (None, 'password123', 422),
    ('fixture_test_user@gmail.com', None, 422)
]) 
def test_incorrect_login(client, create_test_user, email, password, status_code):
    res = client.post("/login", data={'username': email, 'password': password}) # pass in invalid credentials
    assert res.status_code == status_code # 422 - schema validation failed