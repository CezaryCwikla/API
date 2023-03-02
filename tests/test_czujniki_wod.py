# def test_get_authors_no_records(client):
#     response = client.get('/api/v1/czujniki')
#     expected_result = {
#         'success': True,
#         'Zbiór czujników': []
#     }
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#     assert response.get_json() == expected_result


def test_get_czujniki_wod_v1_with_records(client_prod):
    response = client_prod.get('/api/v1/czujniki')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data["Zbiór czujników"]) != 0


def test_get_czujnik_wod_v1(client_prod):
    id = 1
    response = client_prod.get(f'/api/v1/czujniki/{id}')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data["Czujnik"]['id'] == id
    assert response_data["Czujnik"]['alarm'] == 4000
    assert response_data["Czujnik"]['status_id'] == 'active'
    assert response_data["Czujnik"]['warning'] == 2800


def test_get_invalid_czujnik_wod_v1(client_prod):
    id = 100
    response = client_prod.get(f'/api/v1/czujniki/{id}')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == f'Czujnik z id {id} not found'
    assert 'Czujnik' not in response_data


#todo Test czujników wód /v2 (sprawdzanie gdy jest token i gdy nie ma) i /v1 aktualne i historyczne paths
#todo Test czujników powietrza /v1/v2
#todo Testy info