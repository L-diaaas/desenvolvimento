import unittest
from flask import Flask
from turmas.turmas_routes import turmas_blueprint
from turmas.turmas_model import dados, apaga_todas_turmas

class TestTurmasAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração inicial para testar a API"""
        cls.app = Flask(__name__)
        cls.app.register_blueprint(turmas_blueprint)
        cls.client = cls.app.test_client()
        apaga_todas_turmas()  # Limpa os dados antes de iniciar os testes

    def setUp(self):
        """Executado antes de cada teste"""
        apaga_todas_turmas()  # Garante um ambiente limpo para cada teste

    def test_criar_turma_sucesso(self):
        """Testa a criação de uma turma válida"""
        resposta = self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma de História",
            "professor_id": 202,
            "ativo": True
        })
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json["descricao"], "Turma de História")

    def test_criar_turma_dados_invalidos(self):
        """Testa a criação de uma turma sem os dados obrigatórios"""
        resposta = self.client.post('/turmas', json={})
        self.assertEqual(resposta.status_code, 400)

    def test_obter_lista_turmas(self):
        """Testa a obtenção da lista de turmas"""
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma de Matemática",
            "professor_id": 101,
            "ativo": True
        })
        resposta = self.client.get('/turmas')
        self.assertEqual(resposta.status_code, 200)
        self.assertGreater(len(resposta.json), 0)

    def test_obter_turma_existente(self):
        """Testa a obtenção de uma turma específica"""
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma de Geografia",
            "professor_id": 303,
            "ativo": True
        })
        resposta = self.client.get('/turmas/1')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["descricao"], "Turma de Geografia")

    def test_obter_turma_inexistente(self):
        """Testa a busca por uma turma que não existe"""
        resposta = self.client.get('/turmas/99')
        self.assertEqual(resposta.status_code, 404)

    def test_atualizar_turma_sucesso(self):
        """Testa a atualização de uma turma existente"""
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma Antiga",
            "professor_id": 101,
            "ativo": True
        })
        resposta = self.client.put('/turmas/1', json={"descricao": "Turma Atualizada"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["descricao"], "Turma Atualizada")

    def test_atualizar_turma_inexistente(self):
        """Testa a atualização de uma turma inexistente"""
        resposta = self.client.put('/turmas/99', json={"descricao": "Nova Turma"})
        self.assertEqual(resposta.status_code, 404)

    def test_excluir_turma_existente(self):
        """Testa a exclusão de uma turma existente"""
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma para Remover",
            "professor_id": 202,
            "ativo": True
        })
        resposta = self.client.delete('/turmas/1')
        self.assertEqual(resposta.status_code, 204)

    def test_excluir_turma_inexistente(self):
        """Testa a exclusão de uma turma inexistente"""
        resposta = self.client.delete('/turmas/99')
        self.assertEqual(resposta.status_code, 404)

    def test_excluir_todas_turmas(self):
        """Testa a remoção de todas as turmas"""
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma A",
            "professor_id": 111,
            "ativo": True
        })
        self.client.post('/turmas', json={
            "id": 2,
            "descricao": "Turma B",
            "professor_id": 222,
            "ativo": True
        })
        resposta = self.client.delete('/turmas')
        self.assertEqual(resposta.status_code, 200)
        resposta_lista = self.client.get('/turmas')
        self.assertEqual(len(resposta_lista.json), 0)

if __name__ == '__main__':
    unittest.main()
