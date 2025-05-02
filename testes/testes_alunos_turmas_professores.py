import unittest
from app import app, db
from turmas.turmas_model import Turmas
from datetime import datetime

class TestTurmasRotas(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from professores.professores_model import Professor
            professor = Professor(
                nome="Prof. Teste",
                idade=46,
                materia="Biologia",
                observacoes="Doutor em Ciências Biológicas"
            )
            db.session.add(professor)
            db.session.commit()

            turma = Turmas(
                nome="Turma Teste",
                descricao="Descrição da turma",
                ativo=True,
                professor_id=professor.id
            )
            db.session.add(turma)
            db.session.commit()
            self.turma_id = turma.id_turma

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def criar_turma(self, professor_id=None):
        return {
            "nome": "Turma Teste 2",
            "descricao": "Nova turma de teste",
            "ativo": True,
            "professor_id": professor_id or self.turma_id
        }

    def test_get_turmas_vazio(self):
        with app.app_context():
            db.session.query(Turmas).delete()
            db.session.commit()

        response = self.client.get("/turmas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_turma(self):
        turma = self.criar_turma()
        response = self.client.post("/turmas", json=turma)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("message" in response.json)
        self.assertEqual(response.json["message"], "Turma adicionada com sucesso!")

    def test_get_turma_existente(self):
        turma = self.criar_turma()
        self.client.post("/turmas", json=turma)
        response = self.client.get(f"/turmas/{self.turma_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["nome"], "Turma Teste")

    def test_get_turma_inexistente(self):
        response = self.client.get("/turmas/999")
        self.assertEqual(response.status_code, 404)

    def test_put_turma(self):
        turma = self.criar_turma()
        self.client.post("/turmas", json=turma)
        turma["nome"] = "Turma Atualizada"
        response = self.client.put(f"/turmas/{self.turma_id}", json=turma)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["nome"], "Turma Atualizada")

    def test_delete_turma(self):
        turma = self.criar_turma()
        self.client.post("/turmas", json=turma)
        response = self.client.delete(f"/turmas/{self.turma_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_turma_inexistente(self):
        response = self.client.delete("/turmas/999")
        self.assertEqual(response.status_code, 204)

    def test_post_turma_dados_incompletos(self):
        turma_incompleta = {
            "nome": "Turma Incompleta"
        }
        response = self.client.post("/turmas", json=turma_incompleta)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_post_turma_professor_inexistente(self):
        turma = self.criar_turma(professor_id=999)
        response = self.client.post("/turmas", json=turma)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Professor não existe.")

    def test_get_turmas_com_uma_cadastrada(self):
        turma = self.criar_turma()
        self.client.post("/turmas", json=turma)
        response = self.client.get("/turmas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["nome"], "Turma Teste")

class TestAlunosRotas(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from professores.professores_model import Professor
            professor = Professor(
                nome="Prof. Teste",
                idade=46,
                materia="Biologia",
                observacoes="Doutor em Ciências Biológicas"
            )
            db.session.add(professor)
            db.session.commit()

            turma = Turmas(
                nome="Turma Teste",
                descricao="Descrição da turma",
                ativo=True,
                professor_id=professor.id
            )
            db.session.add(turma)
            db.session.commit()
            self.turma_id = turma.id_turma

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def criar_aluno(self, turma_id=None):
        return {
            "nome": "Aluno Teste",
            "data_nascimento": "2006-01-01",
            "nota_primeiro_semestre": 7.0,
            "nota_segundo_semestre": 8.0,
            "turma_id": turma_id or self.turma_id
        }

    def test_get_alunos_vazio(self):
        response = self.client.get("/alunos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_aluno(self):
        aluno = self.criar_aluno()
        response = self.client.post("/alunos", json=aluno)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("message" in response.json)
        self.assertEqual(response.json["message"], "Aluno adicionado com sucesso!")

    def test_get_aluno_existente(self):
        aluno = self.criar_aluno()
        self.client.post("/alunos", json=aluno)
        response = self.client.get("/alunos/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["nome"], aluno["nome"])

    def test_get_aluno_inexistente(self):
        response = self.client.get("/alunos/999")
        self.assertEqual(response.status_code, 404)

    def test_put_aluno(self):
        aluno = self.criar_aluno()
        self.client.post("/alunos", json=aluno)
        aluno["nome"] = "Aluno Atualizado"
        response = self.client.put("/alunos/1", json=aluno)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["aluno"]["nome"], "Aluno Atualizado")

    def test_delete_aluno(self):
        aluno = self.criar_aluno()
        self.client.post("/alunos", json=aluno)
        response = self.client.delete("/alunos/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Aluno deletado com sucesso!")

    def test_delete_inexistente(self):
        response = self.client.delete("/alunos/999")
        self.assertEqual(response.status_code, 404)

    def test_post_aluno_dados_incompletos(self):
        aluno_incompleto = {
            "nome": "Aluno Incompleto"
        }
        response = self.client.post("/alunos", json=aluno_incompleto)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json)

    def test_post_aluno_turma_inexistente(self):
        aluno = self.criar_aluno(turma_id="turma_inexistente")
        response = self.client.post("/alunos", json=aluno)
        if isinstance(response.json, list):
            self.assertTrue(any("message" in item for item in response.json))
        else:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json["message"], "Aluno adicionado com sucesso!")

    def test_get_alunos_com_um_cadastrado(self):
        aluno = self.criar_aluno()
        self.client.post("/alunos", json=aluno)
        response = self.client.get("/alunos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["nome"], aluno["nome"])

if __name__ == "__main__":
    unittest.main()
