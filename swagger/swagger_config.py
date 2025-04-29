def configure_swagger(app):
    from swagger import blueprint as swagger_bp
    app.register_blueprint(swagger_bp)
