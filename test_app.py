import pandas as pd
import json
import unittest
import app



class TestApp(unittest.TestCase):
    
    df = pd.read_csv('aluguel_carros.csv')
    df.iloc[0:0].to_csv('aluguel_carros.csv', index=False, header=True)

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_00_create(self):
        response = self.app.post('/', json={
            "dt_inicio_aluguel": "2023-08-01",
            "dt_fim_aluguel": "2023-08-05",
            "km_rodados_aluguel": 1000,
            "carro_marca_modelo": "CarroTeste",
            "nm_cliente": "Nome Teste",
            "cpf_cliente": "123.456.789-00",
            "valor": 1000
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Dados inseridos com Sucesso!')

    def test_01_read(self):        
        dados_csv = pd.read_csv('aluguel_carros.csv')
        id_get = dados_csv.loc[dados_csv['id_aluguel'] == 1].values.tolist()[0][0]

        response = self.app.get('/', json={
            "id_aluguel": id_get
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), json.dumps({
            "id_aluguel": id_get,
            "dt_inicio_aluguel": "2023-08-01",
            "dt_fim_aluguel": "2023-08-05",
            "km_rodados_aluguel": 1000,
            "carro_marca_modelo": "CARRO TESTE",
            "nm_cliente": "NOME TESTE",
            "cpf_cliente": "123.456.789-00",
            "valor": 1000
        }))

    def test_02_update(self):
        response = self.app.put('/', json={
            "id_aluguel": 1,
            "nome": "João",
            "modelo": "Fiat",
            "data_inicio": "2021-01-01",
            "data_fim": "2021-01-02",
            "valor_diaria": 100
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Dados inseridos com Sucesso!')

    def test_03_delete(self):
        response = self.app.delete('/', json={
            "id_aluguel": 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Exclusão realizada com sucesso!')