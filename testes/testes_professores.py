import unittest
import requests



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
  runTests()