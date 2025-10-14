import os
import sys
from time import sleep

from scripts.batalha_pokemon import *
from scripts.consulta_pokemon import *


def limpar_terminal(tipo, num=1):
    """Limpa o terminal.

    :param tipo: "tudo" para limpar tudo, "linha" para limpar linhas
    :param num: número de linhas a limpar (apenas se tipo for "linha")"""

    if tipo == 'tudo':
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        for _ in range(num):
            sys.stdout.write('\033[F\033[K')
    sys.stdout.flush()


def cabecalho():
    """Limpa o terminal e mostra o cabeçalho do programa."""

    limpar_terminal('tudo')

    print(
        f'\33[31m{6*"-=-"} 🔥 Simulador de batalhas Pokémon! 🔥 {6*"-=-"}\33[0m\n\n\n'
    )


def verifica_numero_entrada(entrada_id):
    """Verifica se a entrada é um número inteiro entre 1 e 1025.

    :param entrada_id: string com a entrada do usuário
    :return: True se for válido, False se não for válido"""

    try:
        if 1 <= int(entrada_id) <= 1025:
            return True
        else:
            return False
    except ValueError:
        return False


def tela_escolher_pokemon():
    r"""Tela para o usuário escolher os pokémons.

    :return: dicionário com os ids dos pokémons escolhidos"""

    while True:
        cabecalho()
        print(
            '\33[33mO Catálogo atual conta com 1025 pokemons, escolha entre 1 e 1025.\33[0m\n'
        )

        dict_escolha_pokemon = {}

        # entrada dos ids e validação
        for i in range(1, 3):
            id_pokemon = input(f'Pokemon {i}: ').strip()

            resultado = verifica_numero_entrada(id_pokemon)
            if resultado is False:
                print('Entrada inválida, tente novamente...')
                sleep(3)
                break

            # incluir o id no dicionário
            dict_escolha_pokemon[f'pokemon{i}'] = id_pokemon

        if resultado is False:
            continue

        # validar se os pokemons são diferentes
        if (
            dict_escolha_pokemon['pokemon1']
            == dict_escolha_pokemon['pokemon2']
        ):
            print(
                '\n\33[33mVocê não pode escolher o mesmo Pokémon, tente novamente...\33[0m'
            )
            sleep(5)
            continue

        return dict_escolha_pokemon


def tela_confirmar_escolhas(dict_escolha_pokemon):
    """Tela para o usuário confirmar as escolhas dos pokémons.

    :param dict_escolha_pokemon: dicionário com os ids dos pokémons escolhidos
    :return: escolha do usuário (1 para batalhar, 2 para alterar)"""

    while True:
        cabecalho()
        print('\33[33mConfirme suas escolhas:\33[0m\n')

        # mostrar as escolhas
        pokemon1 = dict_escolha_pokemon['Data'][0]
        pokemon2 = dict_escolha_pokemon['Data'][1]

        texto_pokemon1 = f"{pokemon1['id']} - {pokemon1['nome'].capitalize()} ({pokemon1['tipo'].capitalize()})"
        texto_pokemon2 = f"{pokemon2['id']} - {pokemon2['nome'].capitalize()} ({pokemon2['tipo'].capitalize()})"

        print(f'{texto_pokemon1:<30} x {texto_pokemon2:>30}')

        # opções para o usuário
        print('\n\n\33[33m1 - Batalhar\n2 - Alterar\33[0m\n')

        escolha_usuario = input('Escolha (1 ou 2): ').strip()

        # validar a escolha do usuário
        if escolha_usuario not in ['1', '2']:
            print('Entrada inválida, tente novamente...')
            sleep(3)
            continue

        return escolha_usuario


def tela_resultado_batalha(dict_resultado_batalha):
    """Tela para mostrar o resultado da batalha.

    :param dict_resultado_batalha: dicionário com o resultado da batalha
    :return: escolha do usuário (1 para nova batalha, 2 para sair)"""

    while True:
        cabecalho()

        # mostrar o resultado
        print(f'{dict_resultado_batalha['pokemon1']:^20} x {dict_resultado_batalha['pokemon2']:^20}\33[0m\n')
        print(f"\33[32m{dict_resultado_batalha['results'][0]}\33[0m\n\n")

        # opções para o usuário
        print('\33[33m1 - Nova batalha\n2 - Sair\33[0m\n')
        escolha_usuario = input('Escolha (1 ou 2): ').strip()

        # validar a escolha do usuário
        if escolha_usuario not in ['1', '2']:
            print('Entrada inválida, tente novamente...')
            sleep(3)
            continue

        return escolha_usuario


def reiniciar_programa(segundos):
    """Reinicia o programa após uma contagem regressiva.

    :param segundos: número de segundos para a contagem regressiva"""

    for i in range(segundos, 0, -1):
        limpar_terminal('linha', 1)
        print(f'Reiniciando em {i} segundos...')
        sleep(1)


if __name__ == '__main__':
    # loop principal
    while True:

        # passo a passo de escolha, consulta, batalha e resultado
        dict_escolha_pokemon = tela_escolher_pokemon()

        dict_infos_pokemon = consultar_pokemon(dict_escolha_pokemon)
        if dict_infos_pokemon is None:
            reiniciar_programa(10)
            continue

        escolha_usuario = tela_confirmar_escolhas(dict_infos_pokemon)
        if escolha_usuario == '2':
            continue

        dict_resultado_batalha = batalhar(dict_infos_pokemon)
        if dict_resultado_batalha is None:
            reiniciar_programa(10)
            continue

        escolha_usuario = tela_resultado_batalha(dict_resultado_batalha)
        if escolha_usuario == '1':
            continue
        else:
            break
