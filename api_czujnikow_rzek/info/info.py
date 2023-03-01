from api_czujnikow_rzek.info import info_bp
from flask import jsonify


@info_bp.route('/', methods=['GET'])
def get_info():
    return jsonify({
        'Dokumentacja': 'https://documenter.getpostman.com/view/20312643/UzBjuU3u',
    })


