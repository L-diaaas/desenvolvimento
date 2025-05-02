from flask_restx import Namespace, Resource, fields
from flask import request
from professores.professores_model import (
    getTodosProfessores, criarProfessor, getPorIdProfessor,
    attProfessor, deletarProfessor, ProfessorNaoEncontrado, criarProfessorErro
)

api = Namespace('professores', description='Operações relacionadas aos professores')

professor_model = api.model('Professor', {
    'nome': fields.String(required=True),
    'idade': fields.Integer(required=True),
    'materia': fields.String(required=True),
    'observacoes': fields.String(required=False)
})

@api.route('')
class ProfessorList(Resource):
    def get(self):
        return getTodosProfessores()

    @api.expect(professor_model)
    def post(self):
        try:
            return criarProfessor(request.json)
        except criarProfessorErro as e:
            api.abort(400, e.mensagem)

@api.route('/<int:idProfessor>')
@api.param('idProfessor', 'ID do professor')
class ProfessorResource(Resource):
    def get(self, idProfessor):
        try:
            return getPorIdProfessor(idProfessor)
        except ProfessorNaoEncontrado:
            api.abort(404, "Professor não encontrado")

    @api.expect(professor_model)
    def put(self, idProfessor):
        try:
            return attProfessor(idProfessor, request.json)
        except ProfessorNaoEncontrado:
            api.abort(404, "Professor não encontrado")

    def delete(self, idProfessor):
        try:
            deletarProfessor(idProfessor)
            return {'message': 'Professor deletado com sucesso'}
        except ProfessorNaoEncontrado:
            api.abort(404, "Professor não encontrado")
