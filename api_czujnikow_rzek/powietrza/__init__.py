from flask import Blueprint

powietrza_bp = Blueprint('powietrza', __name__)

from api_czujnikow_rzek.powietrza import powietrza