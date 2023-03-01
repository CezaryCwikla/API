from flask import Blueprint

powietrza_bp_v1 = Blueprint('powietrza_v1', __name__)

from api_czujnikow_rzek.powietrza_v1 import powietrza