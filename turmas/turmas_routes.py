from flask import Blueprint, request, jsonify
from turmas.turmas_model import (
    Turma_nao_encontrada,
    lista_turmas,
    turma_por_id,
    atualiza_turma,
    adiciona_turma,
    apaga_turma
)

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(lista_turmas()), 200

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return jsonify(turma), 200
    except Turma_nao_encontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    if not data or 'nome' not in data or 'professor_id' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400
    
    message, status_code = adiciona_turma(data)
    return jsonify(message), status_code

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.json
    try:
        atualiza_turma(id_turma, data)
        return jsonify(turma_por_id(id_turma)), 200
    except Turma_nao_encontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        apaga_turma(id_turma)
        return '', 204
    except Turma_nao_encontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
