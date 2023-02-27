from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from api_czujnikow_rzek.auth import auth