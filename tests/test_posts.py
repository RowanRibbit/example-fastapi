
from typing import List
from app import schemas
import pytest

# posts all require authentication, so how do we deal with this with respect to testing?
# Could define a test and pass in client, test_user to gain access to the returned token with client.post('/login'), which is technically valid, but would rather set up a fixture to instead make a request from an API, instead import the OAuth2 method to fake a token

# create some tests posts with a fixture

# get all posts
def test_get_all_posts(authorized_client, create_test_posts):
    res = authorized_client.get('/posts/')
    assert len(res.json()) == len(create_test_posts)
    # validate using a schema to map a list of dicts to list of schema models
    def validate(post):
        return schemas.PostVote(**post)

    posts_map = map(validate, res.json())
    posts = list(posts_map)
    # assert posts[0].Post.id == create_test_posts[0].id
    # won't work as the posts aren't necessarily returned in the same order

    assert res.status_code == 200

def test_unauthorized_get_post(client, create_test_posts):
    res = client.get(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_get_invalid_post_id(authorized_client, create_test_posts):
    res = authorized_client.get(f'/posts/987654')
    print(res.json())
    assert res.status_code == 404

def test_get_post_by_id(authorized_client, create_test_posts):
    res = authorized_client.get(f'/posts/{create_test_posts[0].id}')
    post = schemas.PostVote(**res.json())
    assert post.Post.id == create_test_posts[0].id
    assert post.Post.content == create_test_posts[0].content
    assert res.status_code == 200

# https://youtu.be/0sOvCWFmrtA?t=61155
@pytest.mark.parametrize("title, content, published", [
    ('new title 1', 'new content 1', True),
    ('new title 2', 'new content 2', False),
    ('Pizza', 'Pizza is Nice', True),
    ('Test Defalt', 'Test Create Post Defaul Published', None)
])
def test_create_post(authorized_client, create_test_user, create_test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})
    created_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    if published != False:
        assert created_post.published == True
    else:
        assert created_post.published == False

@pytest.mark.parametrize("title, content, published", [
    ('new title 1', 'new content 1', True),
    ('Test Defalt', 'Test Create Post Defaul Published', None)
])
def test_unauthorized_create_post(client, create_test_user, create_test_posts, title, content, published):
    res = client.post('/posts/', json={"title": title, "content": content, "published": published})
    assert res.status_code == 401

# deleting a post
def test_unauthorized_delete_post(client, create_test_user, create_test_posts):
    res = client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post(authorized_client, create_test_user, create_test_posts):
    res = authorized_client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, create_test_user, create_test_posts):
    res = authorized_client.delete(f'/posts/88888')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, create_test_user, create_test_posts):
    # last post in test_posts is owned by user 2
    res = authorized_client.delete(f'/posts/{create_test_posts[2].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{create_test_posts[0].id}', json=data)
    updated_post = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']

def test_update_other_user_post(authorized_client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[2].id
    }
    res = authorized_client.put(f'/posts/{create_test_posts[2].id}', json=data)
    
    assert res.status_code == 403

def test_update_unauthorized_user_post(client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[2].id
    }
    res = client.put(f'/posts/{create_test_posts[2].id}', json=data)
    
    assert res.status_code == 401
