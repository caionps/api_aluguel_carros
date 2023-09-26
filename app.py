from flask import Flask, request
from datetime import date
import json
import pandas as pd

app = Flask(__name__)

def validar_data(data):
    try:
        date.fromisoformat(data)
        return True
    except ValueError:
        return False


def validar_cpf(cpf):
    if len(cpf) != 14:
        return False
    else: 
        return True

# Aqui se encontra uma função de continuação que utiliza as funções de validação de data e cpf para validar a nova entrada de dados
def validar_aluguel(dados):
    # SUBSTITUIR TODOS OS CAMPOS Q SÃO OBRIGATÓRIOS POR UMA FUNÇÃO LAMBDA COM LIST COMPREHENSION
    if not dados.get('dt_inicio_aluguel'):
        raise ValueError('Data de início do aluguel é obrigatória')
    if not dados.get('dt_fim_aluguel'):
        raise ValueError('Data de fim do aluguel é obrigatória')
    if not dados.get('km_rodados_aluguel'):
        raise ValueError('É necessário indicar a rodagem do carro no aluguel')
    if not dados.get('carro_marca_modelo'):
        raise ValueError('É necessário indicar a marca e o modelo do carro alugado')
    if not dados.get('nm_cliente'):
        raise ValueError('Nome do cliente é obrigatório')
    if not dados.get('cpf_cliente'):
        raise ValueError('CPF do cliente é obrigatório')
    if not dados.get('valor'):
        raise ValueError('Valor é obrigatório')
    if validar_data(dados.get('dt_inicio_aluguel')) == False:
        raise ValueError('O formato da data de início está incorreta')
    if validar_data(dados.get('dt_fim_aluguel')) == False:
        raise ValueError('O formato da data final está incorreta')
    if dados.get('dt_inicio_aluguel') > dados.get('dt_fim_aluguel'):
        raise ValueError('A data de início do aluguel não pode depois da data de fim do aluguel')
    if validar_cpf(dados.get('cpf_cliente')) == False:
        raise ValueError('O CPF está incorreto')    
    return 

# MONAD PARA COLOCAR LISTA EM CAIXA ALTA
def caixa_alta(lista):
    lista_caixa_alta = list(map(lambda x: str(x).upper() if isinstance(x, str) else x, lista)) #Função Lambda
    return lista_caixa_alta


def abre_csv():
    with open('aluguel_carros.csv', 'r') as arquivo_csv:
            dados_csv = pd.read_csv(arquivo_csv)
    return dados_csv 

# CLOSURE PARA GERAR ID 
def id_aux():   
    df = abre_csv() 
    def gerar_id():       
        max_id_aluguel = df['id_aluguel'].max()
        if pd.isna(max_id_aluguel) == True:
            novo_id_aluguel = 1
        else:
            novo_id_aluguel = max_id_aluguel + 1
        return novo_id_aluguel
    return gerar_id()
    
def criar_json(chaves,valores):
    return dict(zip(chaves,valores))

@app.route('/', methods=['POST'])
def create():
    try:
        # Utilização de list comprehension para pegar apenas os valores do json
        json_novo_aluguel = request.get_json()
        validar_aluguel(json_novo_aluguel)
        lista_novo_aluguel = [json_novo_aluguel[key] for key in json_novo_aluguel]

        id_aluguel = id_aux() # Utilização do gerador de IDs

        lista_novo_aluguel.insert(0,id_aluguel)
        lista_novo_aluguel = caixa_alta(lista_novo_aluguel)
        lista_to_df = pd.DataFrame([lista_novo_aluguel], columns=abre_csv().columns)
        novo_csv_df = pd.concat([abre_csv(),lista_to_df])
        novo_csv_df.to_csv('aluguel_carros.csv', index = False)
        return 'Dados inseridos com Sucesso!'     
    except Exception as e:
        return f"Erro 400 - {e}"
       

@app.route('/', methods=['GET'])
def read():
    json_id = request.get_json()
    id_aluguel = json_id.get('id_aluguel')

    df = abre_csv()  
    lista_id = df.loc[df['id_aluguel'] == id_aluguel].values.tolist()
    
    if lista_id == []:
        return 'O id indicado não existe!'
    else:
        lista_colunas = list(df.columns)
        chaves = [chave for chave in lista_colunas]
        json_resposta = criar_json(chaves,lista_id[0])   
        return json.dumps(json_resposta)


@app.route('/', methods=['PUT'])
def update():
    json_update = request.get_json()
    json_update = validar_aluguel(json_update)
    lista_update = [json_update[key] for key in json_update]
    
    df = abre_csv()
    df.loc[df['id_aluguel'] == lista_update[0]] = lista_update
    df.to_csv('aluguel_carros.csv', index = False)

    return 'Update realizado com sucesso'

@app.route('/', methods=['DELETE'])
def delete():
    id_delete = request.get_json().get('id_aluguel')
    df = abre_csv()
    df = df.loc[df['id_aluguel'] != id_delete]
    if df.values.tolist() == []:
        return 'O id indicado não existe!'
    else:
        df.to_csv('aluguel_carros.csv', index = False)
        return 'Exclusão realizada com sucesso!'
