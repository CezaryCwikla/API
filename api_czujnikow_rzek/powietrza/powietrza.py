from flask import jsonify
from webargs.flaskparser import use_args

from api_czujnikow_rzek import db
from api_czujnikow_rzek.modele import DanePowietrza, czujnik_schema, DanePowietrzaSchema, SampleData, sample_schema, SampleDataSchema, danepowietrza_schema
from api_czujnikow_rzek.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination
from api_czujnikow_rzek.powietrza import powietrza_bp


@powietrza_bp.route('/czujniki', methods=['GET'])
def get_czujniki():
    dane = DanePowietrza.query

    # dane, pagination = get_pagination(dane, 'czujniki.get_czujnik_dane')
    dane = DanePowietrzaSchema(many=True).dump(dane)
    return jsonify({
        'success': True,
        'data': dane
    })

