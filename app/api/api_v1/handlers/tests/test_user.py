from app.utils.conftest import client


def test_get_all_users(client):
    print(response)
    response = client.get('/all/')
    assert response.status_code == 200
