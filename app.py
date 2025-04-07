import os
from config import app
from turmas.turmas_routes import turmas_blueprint
from alunos.alunos_rotas import alunos_blueprint 
from professores.professores_routes import professores_bp

app.register_blueprint(alunos_blueprint)
app.register_blueprint(turmas_blueprint)
app.register_blueprint(professores_bp)


if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )