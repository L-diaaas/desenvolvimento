from flask_restx import Namespace, Resource, fields
from flask import request
from turmas.turmas_model import (
    lista_turmas, turma_por_id, adiciona_turma,
    atualiza_turma, apaga_turma, Turma_nao_encontrada
)

api = Namespace('turmas', description='Operações relacionadas às turmas')

turma_model = api.model('Turma', {
    'nome': fields.String(required=True),
    'descricao': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'professor_id': fields.Integer(required=True)
})

@api.route('')
class TurmaList(Resource):
    def get(self):
        return lista_turmas()

    @api.expect(turma_model)
    def post(self):
        return adiciona_turma(request.json)

@api.route('/<int:id_turma>')
@api.param('id_turma', 'ID da turma')
class TurmaResource(Resource):
    def get(self, id_turma):
        try:
            return turma_por_id(id_turma)
        except Turma_nao_encontrada:
            api.abort(404, "Turma não encontrada")

    @api.expect(turma_model)
    def put(self, id_turma):
        try:
            atualiza_turma(id_turma, request.json)
            return turma_por_id(id_turma)
        except Turma_nao_encontrada:
            api.abort(404, "Turma não encontrada")

    def delete(self, id_turma):
        try:
            apaga_turma(id_turma)
            return {'message': 'Turma deletada com sucesso'}
        except Turma_nao_encontrada:
            api.abort(404, "Turma não encontrada")
