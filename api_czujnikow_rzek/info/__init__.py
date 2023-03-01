from flask import Blueprint

info_bp = Blueprint('info', __name__)

from api_czujnikow_rzek.info import info
