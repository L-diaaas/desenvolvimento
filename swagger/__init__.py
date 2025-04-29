from flask_restx import Api
from flask import Blueprint
from swagger.namespace.alunos_namespace import api as alunos_ns
from swagger.namespace.professores_namespace import api as professores_ns
from swagger.namespace.turmas_namespace import api as turmas_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs', title='API Escolar', version='1.0', description='Documentação da API Escolar')

api.add_namespace(alunos_ns, path='/alunos')
api.add_namespace(professores_ns, path='/professores')
api.add_namespace(turmas_ns, path='/turmas')
