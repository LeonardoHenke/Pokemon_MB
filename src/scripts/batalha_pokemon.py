import requests


def batalhar(dict_infos_pokemon):
    '''Envia as informações dos pokémons onde a API Flask responde com o resultado da batalha.

    :param dict_infos_pokemon: dicionário com as informações dos pokémons (id, nome e tipo)
    :return: dicionário com o resultado da batalha'''

    url = 'http://127.0.0.1:5000/battle'

    try:
        response = requests.post(url, json=dict_infos_pokemon, timeout=10)

        # verificar se a resposta é válida
        response.raise_for_status()
        return response.json()['Data'][0]
    
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
