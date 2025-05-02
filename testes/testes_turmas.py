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
        print(response.json)
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

if __name__ == "__main__":
    unittest.main()
