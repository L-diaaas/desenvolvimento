from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno, alunos

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

aluno_id_controle = 1  

@alunos_blueprint.route('/alunos', methods=['POST'])
def adicionar_aluno():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Dados inválidos ou faltando no corpo da requisição."}), 400
        
        global aluno_id_controle
        novo_aluno = {
            "id": aluno_id_controle,  
            "nome": data["nome"],
            "idade": data["idade"],
            "turma_id": data.get("turma_id"),
            "data_nascimento": data.get("data_nascimento"),
            "nota_primeiro_semestre": float(data["nota_primeiro_semestre"]),
            "nota_segundo_semestre": float(data["nota_segundo_semestre"]),
            "media_final": float(data["media_final"])
        }
        alunos["alunos"].append(novo_aluno)  
        aluno_id_controle += 1
        return jsonify(novo_aluno), 201 
    except KeyError as e:
        return jsonify({"message": f"Faltando campo obrigatório: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": f"Erro ao processar os dados: {str(e)}"}), 400
    
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    data = request.get_json()
    try:
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
