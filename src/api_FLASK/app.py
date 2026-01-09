from flask import Flask, jsonify, request, make_response
import requests
from scripts.bd import lista_vantagens_desvantagens



def organiza_resposta(status, dict_escolha_pokemon, i, dados=None):
    ''' Organiza a resposta da API
    
    :param status: código de status da requisição
    :param dict_escolha_pokemon: dicionário com os pokémons escolhidos
    :param i: índice do pokémon (1 ou 2)
    :param dados: dados a serem retornados (opcional)
    :return: resposta formatada em JSON'''

    if dados is None:
        dados = []

    # tratar a mensagem conforme o status
    if status == 200:
        mensagem = 'Sucesso'
    elif status == 422:
        mensagem = f'[{dict_escolha_pokemon[f"pokemon{i}"]}] não é válido'
    elif status == 503:
        mensagem = 'Erro de conexão ao consultar API oficial do Pokémon'
    elif status == 504:
        mensagem = 'Timeout ao consultar API oficial do Pokémon'
    else:
        mensagem = 'Erro ao consultar API oficial do Pokémon'

    # formatar a resposta
    return make_response(
        jsonify({
            'Status': status,
            'StatusMessage': mensagem,
            'Data': dados
        }),
        status
    )


# inicializa o Flask
app = Flask(__name__)
app.json.sort_keys = False


@app.route('/infos_pokemon', methods=['GET'])
def consultar_pokemon():
    '''Rota para consultar as informações dos pokémons escolhidos.
    
    :return: resposta formatada em JSON'''

    dict_escolha_pokemon = request.get_json()

    response_json = []
    for i in range(1, 3):
        status_code = 200
        
        # verificar se o id é válido
        if not str(dict_escolha_pokemon[f'pokemon{i}']).isdigit() or not 1 <= int(dict_escolha_pokemon[f'pokemon{i}']) <= 1025:
            return organiza_resposta(422, dict_escolha_pokemon, i)

        # consultar a API oficial do Pokémon
        url = f"https://pokeapi.co/api/v2/pokemon/{dict_escolha_pokemon[f'pokemon{i}']}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            response = response.json()

            # definir os dados que serão retornados
            id_pokemon = response['id']
            nome = response['name']
            tipo = response['types'][0]['type']['name']

            response_json.append({
                "id": id_pokemon,
                "nome": nome,
                "tipo": tipo
            })

        # tratar erros de requisição
        except requests.exceptions.ConnectionError:
            status_code = 503
        except requests.exceptions.Timeout:
            status_code = 504
        except requests.exceptions.HTTPError:
            status_code = response.status_code
        except requests.exceptions.RequestException:
            status_code = 500

        if status_code != 200:
            return organiza_resposta(status_code, dict_escolha_pokemon, i)

    return organiza_resposta(200, dict_escolha_pokemon, i, response_json)


@app.route('/battle', methods=['POST'])
def batalhar():
    '''Rota para simular a batalha entre os pokémons.

    :return: resposta formatada em JSON'''

    dict_infos_pokemon = request.get_json()


    try:
        tipo_pokemon1 = dict_infos_pokemon['Data'][0]['tipo'].capitalize()
        tipo_pokemon2 = dict_infos_pokemon['Data'][1]['tipo'].capitalize()
        nome_pokemon1 = dict_infos_pokemon['Data'][0]['nome'].capitalize()
        nome_pokemon2 = dict_infos_pokemon['Data'][1]['nome'].capitalize()
    except (KeyError, IndexError) as e:
        return make_response(jsonify({
            "Status": 400,
            "StatusMessage": f"Erro nos dados recebidos: {str(e)}",
            "Data": []
        }), 400)


    # definir o vencedor conforme as vantagens/desvantagens
    vantagem1 = False
    vantagem2 = False

    if tipo_pokemon2 in lista_vantagens_desvantagens[tipo_pokemon1]['strong_against']:
        vantagem1 = True
    if tipo_pokemon1 in lista_vantagens_desvantagens[tipo_pokemon2]['strong_against']:
        vantagem2 = True

    if vantagem1 is True and vantagem2 is False:
        vencedor_tipo = tipo_pokemon1
        vencedor_nome = nome_pokemon1
        perdedor_tipo = tipo_pokemon2
    elif vantagem2 is True and vantagem1 is False:
        vencedor_tipo = tipo_pokemon2
        vencedor_nome = nome_pokemon2
        perdedor_tipo = tipo_pokemon1
    else:
        vencedor_nome = None

    if vencedor_nome is not None:
        resultado = [f'{vencedor_tipo.capitalize()} tem vantagem sobre {perdedor_tipo.capitalize()}. {vencedor_nome} vence!']
    else:
        resultado = ['Nenhum dos tipos tem vantagem. Empate!']
        

    # formatar a resposta
    dict_resultado_batalha = {
        "pokemon1": dict_infos_pokemon['Data'][0]['nome'].capitalize(),
        "pokemon2": dict_infos_pokemon['Data'][1]['nome'].capitalize(),
        "results": resultado
    }

    return make_response(jsonify({
        "Status": 200,
        "StatusMessage": "Batalha concluída com sucesso.",
        "Data": [dict_resultado_batalha]
    }), 200)
    


if __name__ == '__main__':
    app.run()

