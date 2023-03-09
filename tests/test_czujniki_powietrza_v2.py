# def test_get_authors_no_records(client):
#     response = client.get('/api/v2/czujniki')
#     expected_result = {
#         'success': True,
#         'Zbiór czujników': []
#     }
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#     assert response.get_json() == expected_result
import datetime
import pytest


def test_get_czujniki_powietrza_v2_missing_token(client_prod):
    response = client_prod.get('/api/v2/powietrza/czujniki')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Zbiór czujników' not in response_data


def test_get_czujniki_powietrza_v2_wrong_token(client_prod):
    response = client_prod.get('/api/v2/powietrza/czujniki',
                               headers={
                                    'Authorization': '123'
                               })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Zbiór czujników' not in response_data


def test_get_czujniki_powietrza_v2_with_records(client_prod, token):
    response = client_prod.get('/api/v2/powietrza/czujniki',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data["Zbiór czujników"]) != 0


@pytest.mark.parametrize('id', [345, 346, 347, 348, 349, 350, 351, 352, 374, 376, 377, 378, 379])
def test_get_czujnik_powietrza_v2(client_prod, id, token):
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['ID'] == id
    assert 'ADRES' in response_data["Czujnik"]
    assert 'DL_G' in response_data["Czujnik"]
    assert 'SZ_G' in response_data["Czujnik"]


def test_get_invalid_czujnik_powietrza_v2(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data


@pytest.mark.parametrize('id', [345, pytest.param(346, marks=pytest.mark.xfail), 347, 348, 349, 350, 351, 352, 374, 376, 377, 378, 379])
def test_get_czujnik_powietrza_v2_aktualne(client_prod, id, token):
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}/aktualne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    today = datetime.date.today().strftime("%Y-%m-%d")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['ID'] == id
    assert 'ADRES' in response_data["Czujnik"]
    assert 'DL_G' in response_data["Czujnik"]
    assert 'SZ_G' in response_data["Czujnik"]
    assert 'Ostatni pomiar PM' in response_data
    assert 'Ostatni pomiar Zanieczyszczen' in response_data
    assert 'Ostatni pomiar pogodowy' in response_data
    assert 'Ostatni pomiar halasu' in response_data
    assert response_data['Ostatni pomiar PM']["device_id"] == id
    assert response_data['Ostatni pomiar PM']["measurement_time"][:10] == today
    assert response_data['Ostatni pomiar Zanieczyszczen']["device_id"] == id
    assert response_data['Ostatni pomiar Zanieczyszczen']["measurement_time"][:10] == today
    assert response_data['Ostatni pomiar pogodowy']["device_id"] == id
    assert response_data['Ostatni pomiar pogodowy']["measurement_time"][:10] == today
    assert response_data['Ostatni pomiar halasu']["device_id"] == id

def test_get_invalid_czujnik_powietrza_v2_aktualne(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}/aktualne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data


@pytest.mark.parametrize('id', [345, pytest.param(346, marks=pytest.mark.xfail), 347, 348, 349, 350, 351, 352, 374, 376, 377, 378, 379])
def test_get_czujnik_powietrza_v2_historyczne(client_prod, id, token):
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}/historyczne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    today = datetime.date.today().strftime("%Y-%m-%d")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['ID'] == id
    assert 'ADRES' in response_data["Czujnik"]
    assert 'DL_G' in response_data["Czujnik"]
    assert 'SZ_G' in response_data["Czujnik"]
    assert 'Dane pogodowe z ostatnich 24 godzin' in response_data
    assert 'Dane PM z ostatnich 24 godzin' in response_data
    assert 'Dane Zanieczyszczen z ostatnich 24 godzin' in response_data
    assert 'Dane Halasu z ostatnich 24 godzin' in response_data
    assert response_data['Dane PM z ostatnich 24 godzin'][-1]["device_id"] == id
    assert response_data['Dane PM z ostatnich 24 godzin'][-1]["measurement_time"][:10] == today
    assert response_data['Dane Zanieczyszczen z ostatnich 24 godzin'][-1]["device_id"] == id
    assert response_data['Dane Zanieczyszczen z ostatnich 24 godzin'][-1]["measurement_time"][:10] == today
    assert response_data['Dane pogodowe z ostatnich 24 godzin'][-1]["device_id"] == id
    assert response_data['Dane pogodowe z ostatnich 24 godzin'][-1]["measurement_time"][:10] == today
    assert len(response_data['Dane pogodowe z ostatnich 24 godzin']) > 1400
    assert len(response_data['Dane pogodowe z ostatnich 24 godzin']) < 1600
    assert len(response_data['Dane PM z ostatnich 24 godzin']) > 1400
    assert len(response_data['Dane PM z ostatnich 24 godzin']) < 1600
    assert len(response_data['Dane Zanieczyszczen z ostatnich 24 godzin']) > 1400
    assert len(response_data['Dane Zanieczyszczen z ostatnich 24 godzin']) < 1600

    assert isinstance(response_data['Dane PM z ostatnich 24 godzin'][-1]["pm1"], float)
    assert isinstance(response_data['Dane PM z ostatnich 24 godzin'][-1]["pm25"], float)
    assert isinstance(response_data['Dane PM z ostatnich 24 godzin'][-1]["pm10"], float)


def test_get_invalid_czujnik_powietrza_v2_historyczne(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v2/powietrza/czujniki/{id}/historyczne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data

