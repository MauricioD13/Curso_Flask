import unittest
from flask import request, redirect, render_template, session, make_response
from flask_login import login_required

from app import create_app
from app.firestore_service import get_users, get_to_dos


app = create_app()


@app.cli.command()
def test():
    """Usa la libreria unittest para correr scripts para hacer testing
    Todos los scripts que se encuentren en la carpeta test y 
    comiencen con test serán ejecutados
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)  # Manejo de error de la pagina
def not_found(error):
    # El argumento indica el numero identificador del error HTTP
    return render_template('Error_404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('Error_500.html', error=error)


@app.route('/')
def index():
    """Función que extrae la información de la IP del usuario

    Returns:
        Response: Respuesta html que redireccione a la ruta 'hello'
    """
    user_ip = request.remote_addr
    response = make_response(redirect('hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    """Método que se usa para:
    - Crear una sesion y guardar la ip del usuario 
    - Crear una instancia que contiene un formulario
    Returns:
        [method]:Pasar parametros por medio de un diccionario al html y renderizar HTML 
    """
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'to_do': get_to_dos(user_id='mauro'),
        'username': username
    }

    users = get_users()

    return render_template('hello.html', **context)


@app.route('/server')
def serv_error():
    raise (Exception('500 error'))
    # Es necesario apagar el modo debug para que funcione
