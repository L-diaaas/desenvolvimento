from config import db
from datetime import datetime, date

class Turmas(db.Model):
    __tablename__ = "turmas"

    id_turma = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    professor = db.relationship('Professor', back_populates='turmas')

    def __init__(self, nome, descricao, ativo, professor_id):
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo
        self.professor_id = professor_id

    def to_dict(self):
        return {
            'id': self.id_turma,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'professor_id': self.professor_id
        }

class Turma_nao_encontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise Turma_nao_encontrada(f'Turma não encontrada.')
    return turma.to_dict()

def lista_turmas():
    turmas = Turmas.query.all()
    return [turma.to_dict() for turma in turmas]

def adiciona_turma(novos_dados):
    from professores.professores_model import Professor 
    professor = Professor.query.get(novos_dados['professor_id'])
    if professor is None:
        return {"message": "Professor não existe."}, 404

    nova_turma = Turmas(
        nome=novos_dados['nome'],
        descricao=novos_dados['descricao'],
        ativo=bool(novos_dados['ativo']),
        professor_id=int(novos_dados['professor_id'])
    )

    db.session.add(nova_turma)
    db.session.commit()
    return {"message": "Turma adicionada com sucesso!"}, 201

def turma_existe(id_turma):
    try:
        turma_por_id(id_turma)
        return True
    except Turma_nao_encontrada:
        return False

def atualiza_turma(id_turma, novos_dados):
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise Turma_nao_encontrada

    turma.nome = novos_dados['nome']
    turma.descricao = novos_dados['descricao']
    turma.ativo = novos_dados['ativo']
    turma.professor_id = novos_dados['professor_id']

    db.session.commit()

def apaga_turma(id_turma):
    turma = Turmas.query.get(id_turma)
    if turma:
        db.session.delete(turma)
        db.session.commit()
