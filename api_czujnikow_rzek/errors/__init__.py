from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from api_czujnikow_rzek.errors import errors