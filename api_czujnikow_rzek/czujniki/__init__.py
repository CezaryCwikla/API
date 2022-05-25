from flask import Blueprint

czujniki_bp = Blueprint('czujniki', __name__)

from api_czujnikow_rzek.czujniki import czujniki
