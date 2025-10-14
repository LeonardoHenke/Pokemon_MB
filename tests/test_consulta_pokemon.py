import pytest
import requests
from scripts.consulta_pokemon import consultar_pokemon



# Mock para requests.get
class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}
    def json(self):
        return self._json_data
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Status code: {self.status_code}")

def test_consultar_pokemon_sucesso(monkeypatch):
    # Mockar requests.get para sucesso
    def mock_get(*args, **kwargs):
        return MockResponse(200, {"id": 1, "nome": "bulbasaur", "tipo": "grass"})
    monkeypatch.setattr(requests, "get", mock_get)

    entrada = {"pokemon1": 1, "pokemon2": 2}
    resultado = consultar_pokemon(entrada)
    assert resultado == {"id": 1, "nome": "bulbasaur", "tipo": "grass"}

def test_consultar_pokemon_connection_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Falha de conexão")
    monkeypatch.setattr(requests, "get", mock_get)

    entrada = {"pokemon1": 1, "pokemon2": 2}
    resultado = consultar_pokemon(entrada)
    assert resultado is None

def test_consultar_pokemon_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Timeout na requisição")
    monkeypatch.setattr(requests, "get", mock_get)

    entrada = {"pokemon1": 1, "pokemon2": 2}
    resultado = consultar_pokemon(entrada)
    assert resultado is None

def test_consultar_pokemon_http_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(404)
    monkeypatch.setattr(requests, "get", mock_get)

    entrada = {"pokemon1": 1, "pokemon2": 2}
    resultado = consultar_pokemon(entrada)
    assert resultado is None

def test_consultar_pokemon_generic_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Erro genérico")
    monkeypatch.setattr(requests, "get", mock_get)

    entrada = {"pokemon1": 1, "pokemon2": 2}
    resultado = consultar_pokemon(entrada)
    assert resultado is None