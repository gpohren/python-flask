from flask import Flask
from .routes.usuario import usuario
from .routes.produto import produto
from .extensions import database
from .commands.userCommands import userCommands
from .commands.productCommands import productCommands

def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(usuario)
    app.register_blueprint(produto)

    app.register_blueprint(userCommands)
    app.register_blueprint(productCommands)
    database.init_app(app)
    return app