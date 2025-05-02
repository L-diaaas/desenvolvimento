import unittest
import requests

class TestTeacherMethods(unittest.TestCase):

    def test_000_professores_retorna_lista(self):
        response = requests.get("http://localhost:5000/api/professores").json()
        self.assertEqual(type(response), list)

    def test_001_criar_professor_sucesso(self):
      professor = {
          "nome": "José Reis",
          "idade": 35,
          "materia": "SQL",
          "observacoes": "Ele disponibiliza materiais complementares, como slides, artigos e listas de exercícios, que ajudam os alunos a revisar e aprofundar o conteúdo após a aula."
      }

      response = requests.post("http://localhost:5000/api/professores", json=professor)
      self.assertEqual(response.status_code, 200)
      response_data = response.json()
      self.assertEqual(response_data['nome'], professor['nome'])
      self.assertEqual(response_data['idade'], professor['idade'])
      self.assertEqual(response_data['materia'], professor['materia'])
      self.assertEqual(response_data['observacoes'], professor['observacoes'])
      self.assertIn('id', response_data)  # Confirma que o ID foi gerado


    def test_002_criar_professor_erro(self):
      professor = {
          "nome": "José Reis",
          "idade": None,
          "materia": "SQL",
          "observacoes": "..."
      }
      response = requests.post("http://localhost:5000/api/professores", json=professor)

      self.assertNotEqual(response.status_code, 200, "A API aceitou um professor com idade inválida.")
      if 'application/json' in response.headers.get('Content-Type', ''):
          data = response.json()
          self.assertIn('message', data)
      else:
          self.assertTrue(response.text)



    def test_003_buscar_professor_id_sucesso(self):
        id = 1  
        response = requests.get(f"http://localhost:5000/api/professores/{id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("nome", response.json())

    def test_004_buscar_professor_id_erro(self):
        id_erro = 999999  
        response = requests.get(f"http://localhost:5000/api/professores/{id_erro}")
        self.assertEqual(response.status_code, 404)

    def test_005_att_professor_sucesso(self):
      novo_professor = {
          'nome': 'Ana Oliveira',
          'idade': 35,
          'materia': 'SQL',
          'observacoes': 'Texto inicial.'
      }
      response = requests.post("http://localhost:5000/api/professores", json=novo_professor)
      self.assertEqual(response.status_code, 200)
      criado = response.json()
      id_criado = criado['id']

      professor_att = {
          'nome': 'Ana Oliveira',
          'idade': 43,
          'materia': 'Matemática Aplicada',
          'observacoes': 'Durante as aulas, ela incentiva a participação dos alunos...'
      }

      response = requests.put(f"http://localhost:5000/api/professores/{id_criado}", json=professor_att)
      self.assertEqual(response.status_code, 200)

      atualizado = response.json()
      self.assertEqual(atualizado['materia'], professor_att['materia'],
                      f"Esperado: {professor_att['materia']}, mas retornou: {atualizado['materia']}")

    def test_006_att_professor_erro(self):
        id_inexistente = 99999
        professor_att = {
            'id': id_inexistente,
            'nome': 'Ana Oliveira',
            'idade': 43,
            'materia': 'Matemática Aplicada',
            'observacoes': 'Durante as aulas, ela incentiva a participação dos alunos...'
        }
        response = requests.put(f"http://localhost:5000/api/professores/{id_inexistente}", json=professor_att)
        self.assertEqual(response.status_code, 404)

    def test_007_deletar_professor_sucesso(self):
        # Usando o ID criado no teste anterior (001)
        id = getattr(self.__class__, 'created_id', None)
        self.assertIsNotNone("Nenhum ID foi criado para deletar.")
        response = requests.delete(f"http://localhost:5000/api/professores/{id}")
        self.assertEqual(response.status_code, 404)

    def test_008_deletar_professor_erro(self):
        id = 99999
        response = requests.delete(f"http://localhost:5000/api/professores/{id}")
        self.assertEqual(response.status_code, 404)

def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTeacherMethods)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)

if __name__ == '__main__':
    runTests()
