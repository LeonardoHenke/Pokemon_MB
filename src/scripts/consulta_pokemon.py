import requests


def consultar_pokemon(dict_escolha_pokemon):
    '''Consulta as informações dos pokémons escolhidos na API Flask.
    
    :param dict_escolha_pokemon: dicionário com os ids dos pokémons escolhidos
    :return: dicionário com as informações dos pokémons (id, nome e tipo) ou None em caso de erro'''

    url = 'http://127.0.0.1:5000/infos_pokemon'
    
    try:
        response = requests.get(url, json=dict_escolha_pokemon, timeout=10)

        # verificar se a resposta é válida
        response.raise_for_status()
        return response.json()
    
    # tratar erros de requisição
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}\nVerificar se o servidor Flask está ligado")
    except requests.exceptions.Timeout as e:
        print(f"Erro de timeout: {e}\nO servidor demorou muito para responder")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

    return None

