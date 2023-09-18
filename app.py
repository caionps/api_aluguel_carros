from flask import Flask, request
from datetime import date
import csv
import pandas as pd

app = Flask(__name__)

def validar_data(data):
    try:
        date.fromisoformat(data)
        return True
    except ValueError:
        return False

def validar_cpf(cpf):
    return cpf

# Aqui se encontra uma função de continuação que utiliza as funções de validação de data e cpf para validar a nova entrada de dados
def validar_novo_aluguel(dados):
    # SUBSTITUIR TODOS OS CAMPOS Q SÃO OBRIGATÓRIOS POR UMA FUNÇÃO LAMBDA COM LIST COMPREHENSION
    if not dados.get("dt_inicio_aluguel"):
        raise ValueError("Data de início do aluguel é obrigatória")
    if not dados.get("dt_fim_aluguel"):
        raise ValueError("Data de fim do aluguel é obrigatória")
    if not dados.get("km_rodados_aluguel"):
        raise ValueError("É necessário indicar a rodagem do carro no aluguel")
    if not dados.get("carro"):
        raise ValueError("Carro é obrigatório")
    if not dados.get("nm_cliente"):
        raise ValueError("Nome do cliente é obrigatório")
    if not dados.get("cpf_cliente"):
        raise ValueError("CPF do cliente é obrigatório")
    if not dados.get("valor"):
        raise ValueError("Valor é obrigatório")
    if validar_data(dados.get("dt_inicio_aluguel")) == False:
        raise ValueError("O formato da data de início está incorreta")
    if validar_data(dados.get("dt_fim_aluguel")) == False:
        raise ValueError("O formato da data final está incorreta")
    if dados.get("dt_inicio_aluguel") > dados.get("dt_fim_aluguel"):
        raise ValueError("A data de início do aluguel não pode depois da data de fim do aluguel")
    if validar_cpf(dados.get("cpf_cliente")) == False:
        raise ValueError("O CPF está incorreto")
    return dados

# MONAD PARA COLOCAR LISTA EM CAIXA ALTA
def caixa_alta(lista):
    lista_caixa_alta = list(map(lambda x: str(x).upper() if isinstance(x, str) else x, lista)) #Função Lambda
    return lista_caixa_alta

# CLOSURE PARA GERAR ID E VERIFICAR SE O ID ESTÁ NOS DADOS
def id_aux():
    def gerar_id():
        with open('aluguel_carros.csv', 'r') as arquivo_csv:
            dados = pd.read_csv(arquivo_csv)
            id_aluguel = dados['id_aluguel'].max() + 1
        return id_aluguel

gerador_id = id_aux()

# Verificar ID
def verificar_id(id_de_busca):
    with open('aluguel_carros.csv', 'r') as arquivo_csv:
        try:
            dados = pd.read_csv(arquivo_csv)
            if id_de_busca in dados['id_aluguel'].values:
                return True
            return False
        except FileNotFoundError:
            return False 

@app.route('/', methods=['POST'])
def create():
    json_novo_aluguel = request.get_json()
    # Utilização de list comprehension para pegar apenas os valores do json
    lista_novo_aluguel = [json_novo_aluguel[key] for key in json_novo_aluguel]
    json_novo_aluguel = validar_novo_aluguel(json_novo_aluguel)

    with open('aluguel_carros.csv', 'a', newline="") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(lista_novo_aluguel)


@app.route('/', methods=['GET'])
def read():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['PUT'])
def update():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['DELETE'])
def delete():
    return "<p>Hello, World!</p>"
