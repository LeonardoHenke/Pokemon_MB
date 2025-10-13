from api_FLASK.app import app
from scripts.consulta_pokemon import *
from scripts.batalha_pokemon import *
import os
import sys
from time import sleep
import requests



def limpar_terminal(tipo: str, num: int = 1):
    if tipo == "tudo":
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        for _ in range(num):
            sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def cabecalho():
    limpar_terminal("tudo")

    print(f'\33[31m{10*"-=-"} 🔥 Simulador de batalhas Pokémon! 🔥 {10*"-=-"}\33[0m\n\n\n')


def verifica_numero_entrada(entrada_id):
    try:
        if 1 <= int(entrada_id) <= 1025:
            return int(entrada_id)
        else:
            return False
    except ValueError:
        return False


def tela_escolher_pokemon():
    while True:
        cabecalho()
        print("\33[33mO Catálogo atual conta com 1025 pokemons, escolha entre 1 e 1025.\33[0m\n")

        dict_escolha_pokemon = {}

        # entrada dos ids e validação
        for i in range(1, 3):
            id_pokemon = input(f"Pokemon {i}: ").strip()

            resultado = verifica_numero_entrada(id_pokemon)
            if resultado is False:
                print('Entrada inválida, tente novamente...')
                sleep(3)
                break

            # incluindo o id no dicionário
            dict_escolha_pokemon[f"pokemon{i}"] = id_pokemon

        if resultado is False:
            continue


        # validação se os pokemons são diferentes
        if dict_escolha_pokemon["pokemon1"] == dict_escolha_pokemon["pokemon2"]:
            print('Você não pode escolher o mesmo Pokémon, tente novamente...')
            sleep(5)
            continue

        return dict_escolha_pokemon


def tela_confirmar_escolhas(dict_escolha_pokemon):
    while True:
        cabecalho()





if __name__ == "__main__":
    # iniciar o servidor Flask
    app.run()

    while True:
        dict_escolha_pokemon = tela_escolher_pokemon()

        dict_infos_pokemon = consultar_pokemon(dict_escolha_pokemon)

        # tela_confirmar_escolhas(dict_infos_pokemon)
        consultar_pokemon(dict_escolha_pokemon)
