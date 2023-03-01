import os
from pathlib import Path
from dotenv import load_dotenv
import urllib.parse
import cx_Oracle
password = urllib.parse.quote_plus(str(os.environ.get('PASSWORD2')))  # '123%40456
name = urllib.parse.quote_plus(str(os.environ.get('NAME')))
ip = urllib.parse.quote_plus(str(os.environ.get('IP')))
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_6")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
    JWT_EXPIRED = 30


class ProdConfig(Config):
    DB_FILE_PATH = base_dir / 'users.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    SQLALCHEMY_BINDS = {'two': f'mysql://{name}:{password}@{ip}/env_data',
                        'three': os.environ.get('ORACLE_URI'),
                        'four': os.environ.get('SQLALCHEMY_DATABASE_URI')}


# gdybym chcial robic testy np. z Userami (tokeny itp)
class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    DEBUG = True
    TESTING = True


config = {
    'prod': ProdConfig,
    'testing': TestingConfig
}
