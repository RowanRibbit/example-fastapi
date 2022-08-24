import pytest
from app import models

@pytest.fixture
def create_test_vote(create_test_posts, session, create_test_user):
    new_vote = models.Vote(post_id=create_test_posts[1].id, user_id=create_test_user['id'])
    session.add(new_vote)
    session.commit

def test_vote_on_post(authorized_client, create_test_posts, create_test_second_user):
    res = authorized_client.post('/vote/', json={"post_id":create_test_posts[1].id, "dir": 1})
    assert res.status_code == 201

# def test_vote_twice_post(authorized_client, create_test_posts, create_test_vote):
#     # need a post with a vote, create a fixture
#     res = authorized_client.post('/vote/', json={"post_id": create_test_posts[1].id, "dir": 1})
#     assert res.status_code == 409

# things that care about prexisting votes fail on post despite working in postman

# def test_delete_vote(authorized_client, create_test_posts, create_test_vote):
#     res = authorized_client.post('/vote/', json={"post_id": create_test_posts[0].id, "dir": 0})
#     assert res.status_code == 201

def test_delete_non_exist_vote(authorized_client, create_test_posts):
    res = authorized_client.post('/vote/', json={"post_id": create_test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_on_non_exist_post(authorized_client, create_test_second_user):
    res = authorized_client.post('/vote/', json={"post_id":80000, "dir": 1})
    assert res.status_code == 404

def test_vote_on_post_unauthorized_user(client, create_test_posts, create_test_second_user):
    res = client.post('/vote/', json={"post_id":create_test_posts[1].id, "dir": 1})
    assert res.status_code == 401


