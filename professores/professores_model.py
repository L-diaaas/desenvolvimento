from config import db

class Professor(db.Model):
    __tablename__ = "professores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(100), nullable=True)

    turmas = db.relationship('Turmas', back_populates='professor')

    def __init__(self, nome, idade, materia, observacoes):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'idade': self.idade, 'materia': self.materia, 'observacoes': self.observacoes}

class criarProfessorErro(Exception):
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem

class ProfessorNaoEncontrado(Exception):
    pass

def getTodosProfessores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def criarProfessor(dados):
    if not dados.get('nome') or dados.get('idade') is None or not dados.get('materia'):
        raise criarProfessorErro("Campos obrigatórios ausentes ou inválidos.")

    novo_professor = Professor(**dados)
    db.session.add(novo_professor)
    db.session.commit()
    return novo_professor.to_dict()

def getPorIdProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()

def attProfessor(idProfessor, novoProfessor):
    professor = Professor.query.get(idProfessor)
    if not professor:
        raise ProfessorNaoEncontrado
    
    professor.nome = novoProfessor.get('nome', professor.nome)
    professor.idade = novoProfessor.get('idade', professor.idade)
    professor.materia = novoProfessor.get('materia', professor.materia)
    professor.observacoes = novoProfessor.get('observacoes', professor.observacoes)

    db.session.commit()
    return professor.to_dict()

def merge_dicts(dict1, dict2):
    merged = dict1.copy()  
    for key, value in dict2.items():
        if key in merged:
            if merged[key] != value:
                merged[key] = value
        else:
            merged[key] = value  
    return merged

def deletarProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()
    return professor.to_dict()
