from flask import Flask
from api_czujnikow_rzek.modele import User, DanePowietrza
from api_czujnikow_rzek import create_app, db


def test_app(app_prod):
    assert isinstance(app_prod, Flask)
    assert app_prod.config['TESTING'] is False
    assert app_prod.config['DEBUG'] is False#