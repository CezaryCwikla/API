# def test_get_authors_no_records(client):
#     response = client.get('/api/v1/czujniki')
#     expected_result = {
#         'success': True,
#         'Zbiór czujników': []
#     }
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#     assert response.get_json() == expected_result
import datetime
import pytest


def test_get_czujniki_wod_v2_with_records(client_prod, token):
    response = client_prod.get('/api/v2/czujniki',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data["Zbiór czujników"]) != 0


def test_get_czujniki_wod_v2_missing_token(client_prod):
    response = client_prod.get('/api/v2/czujniki')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Zbiór czujników' not in response_data


def test_get_czujniki_wod_v2_wrong_token(client_prod):
    response = client_prod.get('/api/v2/czujniki',
                               headers={
                                    'Authorization': '123'
                               })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Zbiór czujników' not in response_data


@pytest.mark.parametrize('id', [1, 2, 3, 4, 5, 6, 7, pytest.param(8, marks=pytest.mark.xfail), 9])
def test_get_czujnik_wod_v2(client_prod, id, token):
    response = client_prod.get(f'/api/v2/czujniki/{id}',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['id'] == id
    assert response_data["Czujnik"]['status_id'] == 'active'


def test_get_invalid_czujnik_wod_v2(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v2/czujniki/{id}',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data


@pytest.mark.parametrize('id', [1, 2, 3, 4, 5, 6, 7, pytest.param(8, marks=pytest.mark.xfail), 9])
def test_get_czujnik_wod_v2_aktualne(client_prod, id, token):
    response = client_prod.get(f'/api/v2/czujniki/{id}/aktualne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    today = datetime.date.today().strftime("%Y-%m-%d")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['id'] == id
    assert response_data["Czujnik"]['status_id'] == 'active'
    assert 'Ostatni pomiar' in response_data
    assert response_data['Ostatni pomiar']["LoggerID"] == id
    assert isinstance(response_data['Ostatni pomiar']["Value"], int)
    assert response_data['Ostatni pomiar']["DateTime"][:10] == today


def test_get_invalid_czujnik_wod_v2_aktualne(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v2/czujniki/{id}/aktualne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data


@pytest.mark.parametrize('id', [1, 2, 3, 4, 5, 6, 7, pytest.param(8, marks=pytest.mark.xfail), 9])
def test_get_czujnik_wod_v2_historyczne(client_prod, id, token):
    response = client_prod.get(f'/api/v2/czujniki/{id}/historyczne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    today = datetime.date.today().strftime("%Y-%m-%d")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['id'] == id
    assert response_data["Czujnik"]['status_id'] == 'active'
    assert 'Dane z ostatnich 24 godzin' in response_data
    assert response_data['Dane z ostatnich 24 godzin'][-1]["LoggerID"] == id
    assert isinstance(response_data['Dane z ostatnich 24 godzin'][-1]["Value"], int)
    assert response_data['Dane z ostatnich 24 godzin'][-1]["DateTime"][:10] == today
    assert len(response_data['Dane z ostatnich 24 godzin']) > 90
    assert len(response_data['Dane z ostatnich 24 godzin']) < 100


def test_get_invalid_czujnik_wod_v2_historyczne(client_prod, token):
    id = 100
    response = client_prod.get(f'/api/v1/czujniki/{id}/historyczne',
                               headers={
                                    'Authorization': token
                               })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data

