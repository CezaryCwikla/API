import pytest
from api_czujnikow_rzek import create_app, db
from api_czujnikow_rzek.modele import User

###### Powtórzenie z config.py, ale wymagane do działania, bo nie ładuje env
import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
password = urllib.parse.quote_plus(str(os.environ.get('PASSWORD2')))  # '123%40456
name = urllib.parse.quote_plus(str(os.environ.get('NAME')))
ip = urllib.parse.quote_plus(str(os.environ.get('IP')))
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)

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
    app.config['SQLALCHEMY_BINDS']['two'] = f'mysql://{name}:{password}@{ip}/env_data'
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

