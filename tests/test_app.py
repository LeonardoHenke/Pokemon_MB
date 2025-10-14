import pytest
from api_FLASK.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_infos_pokemon_sucesso(client, monkeypatch):
    # Mockar requests.get para a PokeAPI
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"id": 1, "name": "bulbasaur", "types": [{"type": {"name": "grass"}}]}
        def raise_for_status(self):
            pass
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    payload = {"pokemon1": 1, "pokemon2": 2}
    response = client.get("/infos_pokemon", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data["Status"] == 200
    assert data["StatusMessage"] == "Sucesso"
    assert len(data["Data"]) == 2
    assert data["Data"][0]["nome"] == "bulbasaur"
    assert data["Data"][0]["tipo"] == "grass"

def test_infos_pokemon_id_invalido(client):
    payload = {"pokemon1": 0, "pokemon2": 2}  # pokemon1 fora do intervalo válido
    response = client.get("/infos_pokemon", json=payload)
    data = response.get_json()
    assert response.status_code == 422
    assert data["Status"] == 422
    assert "não é válido" in data["StatusMessage"]

def test_infos_pokemon_api_erro(client, monkeypatch):
    # Mockar erro HTTP na PokeAPI
    class MockResponse:
        def __init__(self):
            self.status_code = 404
        def raise_for_status(self):
            raise Exception("Erro HTTP 404")
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    payload = {"pokemon1": 1, "pokemon2": 2}
    response = client.get("/infos_pokemon", json=payload)
    data = response.get_json()
    assert data["Status"] == 404

def test_infos_pokemon_api_timeout(client, monkeypatch):
    def mock_get(*args, **kwargs):
        raise Exception("Timeout")
    monkeypatch.setattr("requests.get", mock_get)
    payload = {"pokemon1": 1, "pokemon2": 2}
    response = client.get("/infos_pokemon", json=payload)
    data = response.get_json()
    assert data["Status"] in [500, 504, 503]

def test_battle_sucesso(client):
    # Testa batalha com dados válidos
    payload = {
        "Data": [
            {"id": 1, "nome": "bulbasaur", "tipo": "grass"},
            {"id": 4, "nome": "charmander", "tipo": "fire"}
        ]
    }
    response = client.post("/battle", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data["Status"] == 200
    assert data["StatusMessage"] == "Batalha concluída com sucesso."
    assert "pokemon1" in data["Data"]
    assert "results" in data["Data"]

def test_battle_dados_invalidos(client):
    # Testa batalha com dados faltando
    payload = {
        "Data": [
            {"id": 1, "nome": "bulbasaur"}  # falta o campo 'tipo'
        ]
    }
    response = client.post("/battle", json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert data["Status"] == 400
    assert "Erro nos dados" in data["StatusMessage"]