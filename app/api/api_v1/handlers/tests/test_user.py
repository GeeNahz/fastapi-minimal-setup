from app.utils.conftest import client


def test_get_all_users(client):
    response = client.get('/user/')
    assert response.status_code == 200
