from flask import Flask, jsonify, request, make_response
import requests
from scripts.bd import lista_vantagens_desvantagens



def organiza_resposta(status, dict_escolha_pokemon, i, dados=None):
    if dados is None:
        dados = []

    # trata a mensagem conforme o status
    if status == 200:
        mensagem = 'Sucesso'
    elif status == 400:
        mensagem = f'[{dict_escolha_pokemon[f"pokemon{i}"]}] não é válido'
    else:
        mensagem = 'Erro ao consultar API oficial do Pokémon'

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
    
    dict_escolha_pokemon = request.get_json()

    response_json = []
    for i in range(1, 3):
        
        # verificar se o id é válido
        if not str(dict_escolha_pokemon[f'pokemon{i}']).isdigit() or not 1 <= int(dict_escolha_pokemon[f'pokemon{i}']) <= 1025:
            return organiza_resposta(400, dict_escolha_pokemon, i)

        url = f"https://pokeapi.co/api/v2/pokemon/{dict_escolha_pokemon[f'pokemon{i}']}"

        response = requests.get(url)

        if response.status_code != 200:
            return organiza_resposta(response.status_code, dict_escolha_pokemon, i)

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

    return organiza_resposta(200, dict_escolha_pokemon, i, response_json)


@app.route('/battle', methods=['POST'])
def batalhar():
    dict_infos_pokemon = request.get_json()

    tipo_pokemon1 = dict_infos_pokemon['Data'][0]['tipo'].capitalize()
    tipo_pokemon2 = dict_infos_pokemon['Data'][1]['tipo'].capitalize()

    # definir o vencedor
    vantagem1 = False
    vantagem2 = False

    if tipo_pokemon2 in lista_vantagens_desvantagens[tipo_pokemon1]['strong_against']:
        vantagem1 = True
    if tipo_pokemon1 in lista_vantagens_desvantagens[tipo_pokemon2]['strong_against']:
        vantagem2 = True

    if vantagem1 is True and vantagem2 is False:
        vencedor_tipo = tipo_pokemon1
        vencedor_nome = dict_infos_pokemon["Data"][0]["nome"].capitalize()
        perdedor_tipo = tipo_pokemon2

    elif vantagem2 is True and vantagem1 is False:
        vencedor_tipo = tipo_pokemon2
        vencedor_nome = dict_infos_pokemon["Data"][1]["nome"].capitalize()
        perdedor_tipo = tipo_pokemon1

    else:
        vencedor_nome = None

    if vencedor_nome is not None:
        resultado = [f'{vencedor_tipo.capitalize()} tem vantagem sobre {perdedor_tipo.capitalize()}. {vencedor_nome} vence!']
    else:
        resultado = ['Nenhum dos tipos tem vantagem. Empate!']
        

    dict_resultado_batalha = {
        "pokemon1": dict_infos_pokemon['Data'][0]['nome'].capitalize(),
        "pokemon2": dict_infos_pokemon['Data'][1]['nome'].capitalize(),
        "results": resultado
    }

    return make_response(jsonify(dict_resultado_batalha), 200)
    


if __name__ == '__main__':
    app.run()

