import os
from pathlib import Path
from dotenv import load_dotenv

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_BINDS = {'two' : os.environ.get('SQLALCHEMY_BINDS')}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5