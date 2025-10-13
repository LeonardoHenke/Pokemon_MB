import requests


def consultar_pokemon(dict_escolha_pokemon):
    url = 'http://127.0.0.1:5000/infos_pokemon'
    
    response = requests.get(url, json=dict_escolha_pokemon)
    if response.status_code == 200:
        return response.json()
    else:
        print('Erro ao consultar Pokémon')
        return None
