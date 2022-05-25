from flask import Blueprint

dane_bp = Blueprint('dane', __name__)

from api_czujnikow_rzek.dane import dane
