import unittest
from flask import Flask
from alunos.alunos_rotas import alunos_blueprint
from alunos.alunos_model import alunos, dados, excluir_aluno


class TestAluno(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(alunos_blueprint)
        self.client = self.app.test_client()

        # Resetando alunos para garantir ambiente limpo
        alunos["alunos"].clear()

    def test_01_adicionar_aluno_valido(self):
        payload = {
            "nome": "João",
            "idade": 20,
            "turma_id": 1,
            "data_nascimento": "2005-05-10",
            "nota_primeiro_semestre": 8.5,
            "nota_segundo_semestre": 7.0,
            "media_final": 7.75
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["nome"], "João")
        self.assertEqual(data["idade"], 20)

    def test_02_faltando_nome(self):
        payload = {
            "idade": 20,
            "turma_id": 1,
            "nota_primeiro_semestre": 8.5,
            "nota_segundo_semestre": 7.0,
            "media_final": 7.75
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Faltando campo obrigatório", response.get_json()["message"])

    def test_03_faltando_idade(self):
        payload = {
            "nome": "Maria",
            "turma_id": 2,
            "nota_primeiro_semestre": 9.0,
            "nota_segundo_semestre": 8.0,
            "media_final": 8.5
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_04_corpo_requisicao_vazio(self):
        response = self.client.post('/alunos', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Dados inválidos", response.get_json()["message"])

    def test_05_corpo_sem_json(self):
        response = self.client.post('/alunos', data="não é json")
        self.assertEqual(response.status_code, 415)

    def test_06_tipo_errado_nota_primeiro_semestre(self):
        payload = {
            "nome": "Carlos",
            "idade": 21,
            "turma_id": 3,
            "nota_primeiro_semestre": "oito",
            "nota_segundo_semestre": 7.5,
            "media_final": 7.75
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_07_media_final_invalida(self):
        payload = {
            "nome": "Ana",
            "idade": 19,
            "turma_id": 2,
            "nota_primeiro_semestre": 9.0,
            "nota_segundo_semestre": 8.0,
            "media_final": "oito"
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_08_nome_vazio(self):
        payload = {
            "nome": "",
            "idade": 18,
            "turma_id": 1,
            "nota_primeiro_semestre": 7.0,
            "nota_segundo_semestre": 8.0,
            "media_final": 7.5
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_09_idade_como_texto(self):
        payload = {
            "nome": "Pedro",
            "idade": "vinte",
            "turma_id": 1,
            "nota_primeiro_semestre": 7.0,
            "nota_segundo_semestre": 6.0,
            "media_final": 6.5
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_10_turma_id_negativo(self):
        payload = {
            "nome": "Paula",
            "idade": 22,
            "turma_id": -1,
            "nota_primeiro_semestre": 7.0,
            "nota_segundo_semestre": 6.0,
            "media_final": 6.5
        }
        response = self.client.post('/alunos', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertLess(data["turma_id"], 0)

    def test_11_excluir_aluno_existente(self):
        resposta = self.client.post('/alunos', json={
            "nome": "Aluno para Deletar",
            "idade": 21,
            "turma_id": 100,
            "data_nascimento": "2003-05-10",
            "nota_primeiro_semestre": 7.0,
            "nota_segundo_semestre": 8.0,
            "media_final": 7.5
        })
        self.assertEqual(resposta.status_code, 201)
        aluno_id = resposta.get_json()["id"]

        delete_resposta = self.client.delete(f'/alunos/{aluno_id}')
        self.assertEqual(delete_resposta.status_code, 200)
        self.assertEqual(delete_resposta.get_json()["message"], "Aluno deletado com sucesso!")

    def test_12_excluir_aluno_inexistente(self):
        resposta = self.client.delete('/alunos/9999')
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json()["message"], "Aluno não encontrado.")


if __name__ == "__main__":
    unittest.main()
