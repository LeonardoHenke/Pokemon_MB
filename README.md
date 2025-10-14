# Simulador de Batalhas Pokémon

Este projeto consiste em um simulador de batalhas Pokémon, desenvolvido para fins de entrevista técnica. O sistema é composto por uma interface de linha de comando (CLI) e uma API Flask, integrando-se à PokeAPI para obtenção dos dados dos pokémons. O usuário pode selecionar dois pokémons, visualizar seus dados e realizar batalhas baseadas em vantagens de tipos.

---

## Estrutura do Projeto

```
Pokemon_MB/
├── Enunciado.pdf             # Enunciado original do desafio
├── requirements.txt          # Dependências do projeto
├── setup.py                  # Script de instalação do pacote
├── src/
│   ├── CLI.py                # Cliente CLI para interação com o usuário
│   ├── api_FLASK/
│   │   └── app.py            # Servidor Flask (API)
│   └── scripts/
│       ├── bd.py             # Lógica de vantagens/desvantagens de tipos
│       ├── consulta_pokemon.py # Consulta de dados dos pokémons via API
│       └── batalha_pokemon.py  # Simulação de batalha via API
├── .gitignore
```

---

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/LeonardoHenke/Pokemon_MB.git
   cd Pokemon_MB
   ```

2. Crie e ative um ambiente virtual (opcional, recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## Como Executar

### 1. Inicie o servidor Flask

No terminal, execute:
```bash
python src/api_FLASK/app.py
```
O servidor será iniciado em `http://127.0.0.1:5000`.

### 2. Execute o cliente CLI

Em outro terminal, execute:
```bash
python src/CLI.py
```
Siga as instruções na tela para escolher os pokémons e realizar batalhas.

---

## Funcionalidades

- **Consulta de Pokémons:** Busca os dados na PokeAPI via endpoint `/infos_pokemon` da API Flask.
- **Simulação de batalha:** Compara os tipos dos pokémons selecionados e determina o vencedor conforme lógica de vantagens/desvantagens em `bd.py`.
- **Interface CLI:** Interação amigável, com validação dos dados de entrada, mensagens de erro e opção de reinício automático em caso de falha de comunicação ou dados inválidos.
- **Tratamento de erros:** Robustez contra problemas de conexão, timeout, entrada inválida e erros inesperados.

---

## Exemplos de Uso

### Escolha de Pokémons
- O CLI solicita a escolha de dois IDs de pokémons (de 1 a 1025).
- A API retorna os dados dos pokémons selecionados.

### Batalha
- O CLI permite confirmar os pokémons e iniciar a batalha.
- O resultado é exibido informando o vencedor ou se houve empate.

---

## Estrutura dos Endpoints

- **GET `/infos_pokemon`**  
  Recebe: `{"pokemon1": id1, "pokemon2": id2}`  
  Retorna dados dos pokémons ou mensagem de erro.

- **POST `/battle`**  
  Recebe:  
  ```json
  {
    "Data": [
      {"id": 1, "nome": "bulbasaur", "tipo": "grass"},
      {"id": 4, "nome": "charmander", "tipo": "fire"}
    ]
  }
  ```
  Retorna: Resultado da batalha.

---

## Observações Técnicas

- O projeto foi desenvolvido para fácil separação entre API e cliente CLI.
- Todas as entradas são validadas para evitar erros e garantir boa experiência ao usuário.
- As funções de integração com API possuem tratamento completo de exceções, promovendo robustez.

---

## Referências

- [PokeAPI](https://pokeapi.co/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## Autor

- Leonardo Henke