import pytest
import requests
from scripts.batalha_pokemon import batalhar

# Mock para requests.post
class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}
    def json(self):
        return self._json_data
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Status code: {self.status_code}")

def test_batalhar_sucesso(monkeypatch):
    # Mockar requests.post para sucesso
    def mock_post(*args, **kwargs):
        return MockResponse(200, {"results": ["Pikachu vence!"]})
    monkeypatch.setattr(requests, "post", mock_post)

    entrada = {"Data": [{"id": 25, "nome": "pikachu", "tipo": "electric"}, {"id": 7, "nome": "squirtle", "tipo": "water"}]}
    resultado = batalhar(entrada)
    assert resultado == {"results": ["Pikachu vence!"]}

def test_batalhar_connection_error(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Falha de conexão")
    monkeypatch.setattr(requests, "post", mock_post)

    entrada = {"Data": [{"id": 25, "nome": "pikachu", "tipo": "electric"}, {"id": 7, "nome": "squirtle", "tipo": "water"}]}
    resultado = batalhar(entrada)
    assert resultado is None

def test_batalhar_timeout(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.Timeout("Timeout na requisição")
    monkeypatch.setattr(requests, "post", mock_post)

    entrada = {"Data": [{"id": 25, "nome": "pikachu", "tipo": "electric"}, {"id": 7, "nome": "squirtle", "tipo": "water"}]}
    resultado = batalhar(entrada)
    assert resultado is None

def test_batalhar_http_error(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse(404)
    monkeypatch.setattr(requests, "post", mock_post)

    entrada = {"Data": [{"id": 25, "nome": "pikachu", "tipo": "electric"}, {"id": 7, "nome": "squirtle", "tipo": "water"}]}
    resultado = batalhar(entrada)
    assert resultado is None

def test_batalhar_generic_error(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Erro genérico")
    monkeypatch.setattr(requests, "post", mock_post)

    entrada = {"Data": [{"id": 25, "nome": "pikachu", "tipo": "electric"}, {"id": 7, "nome": "squirtle", "tipo": "water"}]}
    resultado = batalhar(entrada)
    assert resultado is None