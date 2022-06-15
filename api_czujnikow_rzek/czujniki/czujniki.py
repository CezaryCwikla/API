from flask import jsonify
from datetime import date, timedelta, datetime
from webargs.flaskparser import use_args

from api_czujnikow_rzek import db
from api_czujnikow_rzek.modele import Czujnik, czujnik_schema, CzujnikSchema, SampleData, SampleDataSchema, sample_schema
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
    czujnik = Czujnik.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    return jsonify({
        'success': True,
        'data': czujnik_schema.dump(czujnik)
    })


@czujniki_bp.route('/czujniki/<int:czujnik_id>/aktualne', methods=['GET'])
def get_czujnik_dane_aktualne(czujnik_id: int):
    czujnik = Czujnik.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    czujnik = czujnik_schema.dump(czujnik)
    dane = SampleData.query.order_by(SampleData.id.desc()).first() ##tu chyba nie jest dla czujnika z odpowiednim id
   #dane, pagination = get_pagination(dane, 'czujniki.get_czujnik_dane')
    dane = sample_schema.dump(dane)
    return jsonify({
        'success': True,
        'data': dane
    })


@czujniki_bp.route('/czujniki/<int:czujnik_id>/historyczne', methods=['GET'])
def get_czujnik_dane_historyczne(czujnik_id: int):
    czujnik = Czujnik.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    czujnik = czujnik_schema.dump(czujnik)
    dane = SampleData.query.filter(SampleData.LoggerID == czujnik_id, SampleData.DateTime > datetime.now() - timedelta(hours=25)).all()

   #dane, pagination = get_pagination(dane, 'czujniki.get_czujnik_dane')
    dane = SampleDataSchema(many=True).dump(dane)
    return jsonify({
        'success': True,
        'czujnik': czujnik,
        'data': dane
    })