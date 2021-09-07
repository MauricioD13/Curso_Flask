from flask import Flask, request, redirect, render_template, session, url_for,flash
from flask.globals import session
from flask.helpers import make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app) #Inicializacion de la extension bootstrap
# Ya se tiene acceso a los archivos HTML, CSS y JS 

app.config['SECRET_KEY'] = 'SUPER SECRETO' # Necesario para hacer uso de la sesion


to_do = ['IA: Tarea', 'Tesis: Lecturas', 'PSU: Puente']

class LoginForm(FlaskForm):
    """Clase que permite usar la extension de flask WTF para el 
    uso de formularios

    Args:
        FlaskForm ([class]): Clase padre que se importa desde la extension
    """
    username = StringField('Nombre de usuario: ', validators = [DataRequired()])
    password = PasswordField('Contraseña: ', validators = [DataRequired()])
    submit = SubmitField('Enviar')

@app.cli.command()
def test():
    """Usa la libreria unittest para correr scripts para hacer testing
    Todos los scripts que se encuentren en la carpeta test y 
    comiencen con test serán ejecutados
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)



@app.errorhandler(404) #Manejo de error de la pagina
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

@app.route('/hello', methods = ['GET','POST'])
def hello():
    """Método que se usa para:
    - Crear una sesion y guardar la ip del usuario 
    - Crear una instancia que contiene un formulario
    Returns:
        [method]:Pasar parametros por medio de un diccionario al html y renderizar HTML 
    """
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'to_do' : to_do,
        'login_form': login_form,
        'username': username
    }
    #Esta funcion detecta que el método es POST y que el formulario es valido,
    #cuando esto suceda entonces se ejecutará la función
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con exito')
        return redirect(url_for('index'))
    
    return render_template('hello.html', **context)


@app.route('/server')
def serv_error():
    raise (Exception('500 error'))
    #Es necesario apagar el modo debug para que funcione
