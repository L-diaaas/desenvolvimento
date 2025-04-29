from flask_restx import Namespace, Resource, fields
from flask import request
from alunos.alunos_model import listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno, AlunoNaoEncontrado

api = Namespace('alunos', description='Operações relacionadas aos alunos')

aluno_model = api.model('Aluno', {
    'nome': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'nota_primeiro_semestre': fields.Float(required=True),
    'nota_segundo_semestre': fields.Float(required=True),
    'turma_id': fields.Integer(required=True)
})

@api.route('')
class AlunoList(Resource):
    @api.doc('listar_alunos')
    def get(self):
        return listar_alunos()

    @api.expect(aluno_model)
    @api.doc('adicionar_aluno')
    def post(self):
        data = request.get_json()
        return adicionar_aluno(data)

@api.route('/<int:id_aluno>')
@api.param('id_aluno', 'ID do aluno')
class AlunoResource(Resource):
    def get(self, id_aluno):
        try:
            return aluno_por_id(id_aluno)
        except AlunoNaoEncontrado:
            api.abort(404, "Aluno não encontrado")

    @api.expect(aluno_model)
    def put(self, id_aluno):
        try:
            return atualizar_aluno(id_aluno, request.get_json())
        except AlunoNaoEncontrado:
            api.abort(404, "Aluno não encontrado")

    def delete(self, id_aluno):
        try:
            excluir_aluno(id_aluno)
            return {'message': 'Aluno excluído com sucesso'}
        except AlunoNaoEncontrado:
            api.abort(404, "Aluno não encontrado")
