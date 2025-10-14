import requests


def consultar_pokemon(dict_escolha_pokemon):
    '''Consulta as informações dos pokémons escolhidos na API Flask.
    
    :param dict_escolha_pokemon: dicionário com os ids dos pokémons escolhidos
    :return: dicionário com as informações dos pokémons'''

    url = 'http://127.0.0.1:5000/infos_pokemon'
    
    response = requests.get(url, json=dict_escolha_pokemon)

    # TODO: tratar erros

    return response.json()

