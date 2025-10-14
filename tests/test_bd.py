import pytest
from scripts.bd import lista_vantagens_desvantagens

def test_lista_vantagens_desvantagens_structure():
    # Garante que cada tipo tem campos obrigatórios
    for tipo, dados in lista_vantagens_desvantagens.items():
        assert "strong_against" in dados, f"{tipo} missing strong_against"
        assert isinstance(dados["strong_against"], list)
        # Opcional: pode adicionar outros campos obrigatórios
        # assert "weak_against" in dados

def test_vantagem_entre_tipos():
    # Exemplo: Fire é forte contra Grass
    assert "Grass" in lista_vantagens_desvantagens["Fire"]["strong_against"]
    # Exemplo: Water é forte contra Fire
    assert "Fire" in lista_vantagens_desvantagens["Water"]["strong_against"]
    # Exemplo: Grass não é forte contra Fire
    assert "Fire" not in lista_vantagens_desvantagens["Grass"]["strong_against"]

def test_tipo_inexistente():
    # Garante que acessar tipo inexistente lança KeyError
    with pytest.raises(KeyError):
        _ = lista_vantagens_desvantagens["Ghost"]