from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth
from flask_login import LoginManager
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    """Cada vez que flask quiera cargar el usuario
    para la sesion activa llamara esta funcion de query"""
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app) #Inicializacion de la extension bootstrap
    # Ya se tiene acceso a los archivos HTML, CSS y JS 

    app.config.from_object(Config) # Necesario para hacer uso de la sesion
    
    app.register_blueprint(auth)
    
    return app

