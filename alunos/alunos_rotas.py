from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/alunos', methods=['POST'])
def post_aluno():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Dados inválidos ou ausentes"}), 400
        novo_aluno = adicionar_aluno(data)
        return jsonify({"message": "Aluno adicionado com sucesso!"}), 201  # Alterado para incluir a chave "message"
    except KeyError as e:
        return jsonify({"message": f"Faltando campo obrigatório: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": f"Erro ao processar os dados: {str(e)}"}), 400

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    try:
        data = request.get_json()
        aluno = atualizar_aluno(id_aluno, data)
        return jsonify({"message": "Aluno atualizado com sucesso!", "aluno": aluno})
    except AlunoNaoEncontrado:
        return jsonify({"message": "Aluno não encontrado."}), 404

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return jsonify({"message": "Aluno deletado com sucesso!"}), 200
    except AlunoNaoEncontrado:
        return jsonify({"message": "Aluno não encontrado."}), 404
