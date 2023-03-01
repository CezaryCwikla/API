from flask import jsonify
from datetime import date, timedelta, datetime

from api_czujnikow_rzek import db
from api_czujnikow_rzek.modele import DanePowietrza, czujnik_schema, DanePowietrzaSchema, \
    StacjePowietrzaSchema, StacjePowietrza, stacjepowietrza_schema,\
    SampleData, sample_schema, SampleDataSchema, danepowietrza_schema,\
    DanePMPowietrza, DaneHalasu, DaneZanieczyszczeniaPowietrza,\
    DaneZanieczyszczeniaPowietrzaSchema, DanePMPowietrzaSchema, DaneHalasuSchema,\
    danepmpowietrza_schema, danehalasu_schema, danezanieczyszczenia_schemna
from api_czujnikow_rzek.utils import validate_json_content_type, get_schema_args, apply_order, \
    apply_filter, get_pagination
from api_czujnikow_rzek.powietrza_v1 import powietrza_bp_v1


@powietrza_bp_v1.route('/czujniki', methods=['GET'])
def get_czujniki():
    query = StacjePowietrza.query
    dane = StacjePowietrzaSchema(many=True).dump(query)
    return jsonify({
        'success': True,
        'Zbiór czujników': dane
    })

@powietrza_bp_v1.route('/czujniki/<int:czujnik_id>', methods=['GET'])
def get_czujnik(czujnik_id: int):
    czujnik = StacjePowietrza.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    dane = stacjepowietrza_schema.dump(czujnik)
    return jsonify({
        'success': True,
        'Czujnik': dane
    })


@powietrza_bp_v1.route('/czujniki/<int:czujnik_id>/aktualne', methods=['GET'])
def get_aktualne(czujnik_id: int):
    czujnik = StacjePowietrza.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    czujnik = stacjepowietrza_schema.dump(czujnik)

    danemeteo = DanePowietrza.query.filter(DanePowietrza.device_id == czujnik_id)
    danemeteo = danemeteo.order_by(DanePowietrza.id.desc()).first() ##tu chyba nie jest dla czujnika z odpowiednim id
   #dane, pagination = get_pagination(dane, 'czujniki_v1.get_czujnik_dane')
    danemeteo = danepowietrza_schema.dump(danemeteo)

    danepm = DanePMPowietrza.query.filter(DanePMPowietrza.device_id == czujnik_id)
    danepm = danepm.order_by(DanePMPowietrza.id.desc()).first()
    danepm = danepmpowietrza_schema.dump(danepm)

    danezanieczyszczenia = DaneZanieczyszczeniaPowietrza.query.filter\
        (DaneZanieczyszczeniaPowietrza.device_id == czujnik_id)
    danezanieczyszczenia = danezanieczyszczenia.order_by(DaneZanieczyszczeniaPowietrza.
                                                         id.desc()).first()
    danezanieczyszczenia = danezanieczyszczenia_schemna.dump(danezanieczyszczenia)

    danehalasu = DaneHalasu.query.filter(DaneHalasu.device_id == czujnik_id)
    danehalasu = danehalasu.order_by(DaneHalasu.id.desc()).first()
    danehalasu = danehalasu_schema.dump(danehalasu)



    #

    ### TO DO:
    # dopiero w sumie zrobilem tutaj czesc, jest kwestia potestowania tego
    # nastepnie polaczenia w jedno i stworzenia jakikejs struktury
    # nastepnie pushujemy to live
    #danepm.update(danezanieczyszczenia)
    return jsonify({
        'success': True,
        'Czujnik': czujnik,
        'Ostatni pomiar pogodowy': danemeteo,
        'Ostatni pomiar PM': danepm,
        'Ostatni pomiar Zanieczyszczen': danezanieczyszczenia,
        'Ostatni pomiar halasu': danehalasu

    })


@powietrza_bp_v1.route('/czujniki/<int:czujnik_id>/historyczne', methods=['GET'])
def get_historyczne(czujnik_id: int):
    czujnik = StacjePowietrza.query.get_or_404(czujnik_id, description=f'Czujnik z id {czujnik_id} not found')
    czujnik = stacjepowietrza_schema.dump(czujnik)

    #
    danemeteo = DanePowietrza.query.filter(DanePowietrza.device_id == czujnik_id,
                                      DanePowietrza.measurement_time > datetime.now() - timedelta(hours=25)).all()

    danemeteo = DanePowietrzaSchema(many=True).dump(danemeteo)
    ### TO DO:
    # dopiero w sumie zrobilem tutaj czesc, jest kwestia potestowania tego
    # nastepnie polaczenia w jedno i stworzenia jakikejs struktury
    # nastepnie pushujemy to live
    # danepm.update(danezanieczyszczenia)



    danepm = DanePMPowietrza.query.filter(DanePMPowietrza.device_id == czujnik_id, DanePMPowietrza.measurement_time > datetime.now() - timedelta(hours=25)).all()

    danepm = DanePMPowietrzaSchema(many=True).dump(danepm)

    danezanieczyszczenia = DaneZanieczyszczeniaPowietrza.query.filter(DaneZanieczyszczeniaPowietrza.device_id == czujnik_id,
                                      DaneZanieczyszczeniaPowietrza.measurement_time > datetime.now() - timedelta(hours=25)).all()

    danezanieczyszczenia = DaneZanieczyszczeniaPowietrzaSchema(many=True).dump(danezanieczyszczenia)

    danehalasu = DaneHalasu.query.filter(DaneHalasu.device_id == czujnik_id,
                                      DaneHalasu.measurement_time > datetime.now() - timedelta(hours=25)).all()
    danehalasu = DaneHalasuSchema(many=True).dump(danehalasu)


    return jsonify({
        'success': True,
        'Czujnik': czujnik,
        'Dane pogodowe z ostatnich 24 godzin': danemeteo,
        'Dane PM z ostatnich 24 godzin': danepm,
        'Dane Zanieczyszczen z ostatnich 24 godzin': danezanieczyszczenia,
        'Dane Halasu z ostatnich 24 godzin': danehalasu
    })
