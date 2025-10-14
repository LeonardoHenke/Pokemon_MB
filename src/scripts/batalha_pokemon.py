import requests


def batalhar(dict_infos_pokemon):
    url = 'http://127.0.0.1:5000/battle'
    
    response = requests.post(url, json=dict_infos_pokemon)

    return response.json()