import pytest
from app.models import User, Vote, Post

# very simple initial test
def add(num1: int, num2: int):
    return num1+num2

# assert True - nothing happens, or False - like raising an error for testing purposes
@pytest.mark.parametrize('num1, num2, expected', [(1,3,4), (5,7,12), (13,21,34)])
def test_add(num1, num2, expected):
    print('testing add fn')
    assert add(num1,num2) == expected

# Auto-discovery functionality of Pytest looks for tests with files that start with test_*.py or *_test.py
# 'Pytest' - collected one item, single green dot indicated it passed
# if you don't use naming can run 'pytest {name}'
# Name of test within module matters too with the same autodiscovery, test prefixed text function or method outside a class
# pytest --help, pytest -v for verbose lists out specific tests that ran and passed. Don't see the print statement either, have to pass in '-s' too
# can use the decorator pytest.mark.parameterise('var1, var', [(val1, val2), (val1, val2)...]) to pass in variables (keep in mind all as one string), then followed by a list of tuples

# Pytest has fixtures - a function that runs before specific tests. A fixture is a function that runs before our test
@pytest.fixture
def new_user():
    return User()

def test_user(new_user):
    print(type(new_user))
    assert type(new_user) == User

# if you expect an error, need a different test case, if an exception is raised it expects it to be true
def test_user2(new_user):
    with pytest.raises(Exception):
        assert type(new_user) == Vote

def fake_error():
    raise ZeroDivisionError()

def test_error():
    # with pytest.raises(SystemError):
    with pytest.raises(ZeroDivisionError):
        assert fake_error()