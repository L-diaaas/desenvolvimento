import unittest
import requests
from flask import Flask
from alunos.alunos_rotas import alunos_blueprint
from alunos.alunos_model import alunos, dados, excluir_aluno
from turmas.turmas_routes import turmas_blueprint
from turmas.turmas_model import apaga_todas_turmas


# Instalar o requirements com: pip install -r requirements.txt
# Para rodar esse teste digite no terminal: python -m unittest -v testes.testes_alunos_turmas_professores

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


class TestTurmasAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(turmas_blueprint)
        cls.client = cls.app.test_client()
        apaga_todas_turmas()

    def setUp(self):
        apaga_todas_turmas()

    def test_criar_turma_sucesso(self):
        resposta = self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma de História",
            "professor_id": 202,
            "ativo": True
        })
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json["descricao"], "Turma de História")

    def test_criar_turma_dados_invalidos(self):
        resposta = self.client.post('/turmas', json={})
        self.assertEqual(resposta.status_code, 400)

    def test_obter_lista_turmas(self):
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
        resposta = self.client.get('/turmas/99')
        self.assertEqual(resposta.status_code, 404)

    def test_atualizar_turma_sucesso(self):
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
        resposta = self.client.put('/turmas/99', json={"descricao": "Nova Turma"})
        self.assertEqual(resposta.status_code, 404)

    def test_excluir_turma_existente(self):
        self.client.post('/turmas', json={
            "id": 1,
            "descricao": "Turma para Remover",
            "professor_id": 202,
            "ativo": True
        })
        resposta = self.client.delete('/turmas/1')
        self.assertEqual(resposta.status_code, 204)

    def test_excluir_turma_inexistente(self):
        resposta = self.client.delete('/turmas/99')
        self.assertEqual(resposta.status_code, 404)

    def test_excluir_todas_turmas(self):
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
    
class TestTeacherMethods(unittest.TestCase):
  
  def test_000_professores_retorna_lista(self):
    response = requests.get('http://localhost:5000/professores').json()
    self.assertEqual(type(response), type([]))
    
  def test_001_criar_professor_sucesso(self):
    professor = {
      "id": 1028,
      "nome": "José Reis",
      "idade": 35,
      "materia": "SQL",
      "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
    }
    
    response = requests.post("http://localhost:5000/professores",json=professor) 
    print(response)
    self.assertEqual(response.json(), professor)
   
  def test_002_criar_professor_erro(self):
    professor = {
      "id": None,
      "nome": "José Reis",
      "idade": 35,
      "materia": "SQL",
      "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
    }
    response = requests.post("http://localhost:5000/professores",json=professor)
    self.assertEqual(response.status_code,400)
    response_data = response.json()
    self.assertEqual(response_data['mensagem'], "O campo 'id' é obrigatório e deve estar preenchido.")
  
    professor = {
      "id": 1502,
      "nome": None,
      "idade": 35,
      "materia": "SQL",
      "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
    }
    response = requests.post("http://localhost:5000/professores",json=professor)
    self.assertEqual(response.status_code,400)
    response_data = response.json()
    self.assertEqual(response_data['mensagem'], "O campo 'nome' é obrigatório e deve estar preenchido.")
    professor = {
      "id": 1502,
      "nome": "José Reis",
      "idade": None,
      "materia": "SQL",
      "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
    }
    response = requests.post("http://localhost:5000/professores",json=professor)
    self.assertEqual(response.status_code,400)
    response_data = response.json()
    self.assertEqual(response_data['mensagem'], "O campo 'idade' é obrigatório e deve estar preenchido.")
    professor = {
      "id": 1502,
      "nome": "José Reis",
      "idade": 35,
      "materia": None,
      "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
    }
    response = requests.post("http://localhost:5000/professores",json=professor)
    self.assertEqual(response.status_code,400)
    response_data = response.json()
    self.assertEqual(response_data['mensagem'], "O campo 'materia' é obrigatório e deve estar preenchido.")
    
  def test_003_buscar_professor_id_sucesso(self):
    id = 1023
    response = requests.get(f"http://localhost:5000/professores/{id}")
    professor = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertIsNotNone(professor)
    self.assertEqual(professor['nome'], "Lucas Silva")
    
  def test_004_buscar_professor_id_erro(self):
    id = 1029
    response = requests.get(f"http://localhost:5000/professores/{id}")
    self.assertEqual(response.status_code, 404)

  def test_005_att_professor_sucesso(self):
    professor_att = {
      'id': 1024,
      'nome': 'Ana Oliveira',
      'idade': 43,
      'materia': 'Matemática Aplicada',
      'observacoes': 'Durante as aulas, ela incentiva a participação dos alunos, fazendo perguntas e promovendo discussões para garantir que todos acompanhem o ritmo.'
    }
    response = requests.put(f"http://localhost:5000/professores/{professor_att['id']}",json=professor_att)
    self.assertEqual(response.status_code,200)
    self.assertEqual(response.json(),professor_att)

  def test_006_att_professor_erro(self):
    professor_att = {
      'id': 1400,
      'nome': 'Ana Oliveira',
      'idade': 43,
      'materia': 'Matemática Aplicada',
      'observacoes': 'Durante as aulas, ela incentiva a participação dos alunos, fazendo perguntas e promovendo discussões para garantir que todos acompanhem o ritmo.'
    }
    response = requests.put(f"http://localhost:5000/professores/{professor_att['id']}",json=professor_att)
    self.assertEqual(response.status_code,400)

  def test_007_deletar_professor_sucesso(self):
    professor_removido = {
        'id': 1025,
        'nome': 'Pedro Santos',
        'idade': 30,
        'materia': 'Estrutura de Dados',
        'observacoes': 'Ele costuma apresentar exemplos do dia a dia ou casos reais para ajudar na aplicação dos conceitos.'
    }
    requests.post("http://localhost:5000/professores", json=professor_removido)
    response = requests.delete(f"http://localhost:5000/professores/{professor_removido['id']}")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), professor_removido)
 
  def test_008_deletar_professor_erro(self):
    professor_removido = {
        'id': 15,
        'nome': 'Pedro Santos',
        'idade': 30,
        'materia': 'Estrutura de Dados',
        'observacoes': 'Ele costuma apresentar exemplos do dia a dia ou casos reais para ajudar na aplicação dos conceitos.'
    }
    requests.post("http://localhost:5000/professores", json=professor_removido)
    response = requests.delete(f"http://localhost:5000/professores/{professor_removido['id']}")
    self.assertEqual(response.status_code, 400)
 
def runTests():
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTeacherMethods)
  unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    unittest.main()
    runTests()
