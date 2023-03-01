from flask import Blueprint

czujniki_bp_v1 = Blueprint('czujniki_v1', __name__)

from api_czujnikow_rzek.czujniki_v1 import czujniki
