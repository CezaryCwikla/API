from flask import jsonify
from webargs.flaskparser import use_args

from api_czujnikow_rzek import db
from api_czujnikow_rzek.modele import Czujnik, czujnik_schema, CzujnikSchema
from api_czujnikow_rzek.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination
from api_czujnikow_rzek.czujniki import czujniki_bp


@czujniki_bp.route('/czujniki', methods=['GET'])
def get_czujniki():
    query = Czujnik.query
    schema_args = get_schema_args(Czujnik)
    query = apply_order(Czujnik, query)
    query = apply_filter(Czujnik, query)

    items, pagination = get_pagination(query, 'czujniki.get_czujniki')
    czujniki = CzujnikSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': czujniki,
        'number_of_records': len(czujniki),
        'pagination': pagination
    })

@czujniki_bp.route('/czujniki/<int:czujnik_id>', methods=['GET'])
def get_czujnik(czujnik_id: int):
    czujnik = Czujnik.query.get_or_404(czujnik_id, description=f'Autor z id {czujnik_id} not found')
    return jsonify({
        'success': True,
        'data': czujnik_schema.dump(czujnik)
    })
