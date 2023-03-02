import pytest
from api_czujnikow_rzek import create_app, db
from api_czujnikow_rzek.modele import User


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        user = User(username='test1233', password='12441212', email='czareko2@op.pl')
        db.session.add(user)
        db.session.commit()

    yield app
    app.config['DB_FILE_PATH'].unlink(missing_ok=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_prod():
    app = create_app('prod')
    yield app


@pytest.fixture
def client_prod(app_prod):
    with app_prod.test_client() as client_v2:
        yield client_v2


@pytest.fixture
def user(client):
    user = {
        'username': 'test23y',
        'password': '124567',
        'email': 'tes2t@gmail.com'
    }
    client.post('/api/v2/auth/register',
                json=user)
    return user


@pytest.fixture
def token(client, user):
    response = client.post('/api/v2/auth/login',
                           json={
                            'username': user['username'],
                            'password': user['password']
                            })
    return response.get_json()['token']

