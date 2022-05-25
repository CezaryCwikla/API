from flask import jsonify
from webargs.flaskparser import use_args


from api_czujnikow_rzek import db
from api_czujnikow_rzek.modele import Czujnik, czujnik_schema, CzujnikSchema, SampleData, sample_schema, SampleDataSchema
from api_czujnikow_rzek.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination
from api_czujnikow_rzek.dane import dane_bp

@dane_bp.route('/dane', methods=['GET'])
def get_dane():
    dane = SampleData.query.first()
    return jsonify({
        'success': True,
        'data': sample_schema.dump(dane)
    })