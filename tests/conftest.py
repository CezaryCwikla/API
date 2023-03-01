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
def user(client):
    user = {
        'username': 'test23y',
        'password': '124567',
        'email': 'tes2t@gmail.com'
    }
    client.post('/api/v2/auth/register',
                json=user)
    return user