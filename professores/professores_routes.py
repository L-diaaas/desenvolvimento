from flask import Blueprint, request, jsonify
from .professores_model import ProfessorNaoEncontrado, criarProfessorErro, getTodosProfessores, criarProfessor, getPorIdProfessor, attProfessor, merge_dicts, deletarProfessor
professores_bp = Blueprint('professores', __name__)

@professores_bp.route("/professores", methods=['GET'])
def listarTodosProfessores():
  return jsonify(getTodosProfessores())

@professores_bp.route("/professores", methods=["POST"])
def postProfessor():
    dados = request.json
    try:
        return jsonify(criarProfessor(dados))
    except criarProfessorErro as e:
        return jsonify({'message': e.mensagem}), 400

@professores_bp.route("/professores/<int:idProfessor>", methods=['GET'])
def getProfessorId(idProfessor):
    try:
        professor = getPorIdProfessor(idProfessor)
        return jsonify(professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_bp.route("/professores/<int:idProfessor>", methods=['PUT'])
def updateProfessor(idProfessor):
    dados = request.json
    try:
        return jsonify(attProfessor(idProfessor, dados))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 400

@professores_bp.route("/professores/<int:idProfessor>", methods=['DELETE'])
def deleteProfessor(idProfessor):
    try:
        return jsonify(deletarProfessor(idProfessor)), 200
    except ProfessorNaoEncontrado:
            return jsonify({'message': 'Professor não encontrado'}), 400
