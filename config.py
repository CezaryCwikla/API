import os
from pathlib import Path
from dotenv import load_dotenv
import urllib.parse
import cx_Oracle
password = urllib.parse.quote_plus(os.environ.get('PASSWORD2'))  # '123%40456
name = urllib.parse.quote_plus(os.environ.get('NAME'))
ip = urllib.parse.quote_plus(os.environ.get('IP'))
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_6")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_BINDS = {'two' : f'mysql://{name}:{password}@{ip}/env_data',
                        'three' : os.environ.get('ORACLE_URI')}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
