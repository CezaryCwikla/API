import pytest


def test_register(client):
    response = client.post('/api/v2/auth/register',
                           json={
                               'username': 'test23y',
                               'password': '124567',
                               'email': 'tes2t@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'username': 'test', 'password': '123456'}, 'email'),
        ({'username': 'test', 'email': 'test@gmail.com'}, 'password'),
        ({'password': '123456', 'email': 'test@gmail.com'}, 'username'),
    ]
)
def test_register_invalid_data(client, data, missing_field):
    response = client.post('/api/v2/auth/register',
                           json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_register_invalid_content_type(client):
    response = client.post('/api/v2/auth/register',
                           data={
                               'username': 'tes2t23y',
                               'password': '1224567',
                               'email': 'tes22t@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_register_already_used_username(client, user):
    response = client.post('/api/v2/auth/register',
                           json={
                               'username': user['username'],
                               'password': '1224567',
                               'email': 'tes222t@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_register_already_used_email(client, user):
    response = client.post('/api/v2/auth/register',
                           json={
                               'username': 'newst_user',
                               'password': '1224567',
                               'email': user["email"]
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data