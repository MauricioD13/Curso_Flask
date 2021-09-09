import unittest
from flask import request, redirect, render_template, session, flash, make_response, url_for
from flask_login import login_required, current_user

from app import create_app
from app.firestore_service import update_to_do, get_to_dos, put_to_do, delete_to_do
from app.forms import To_doForm, DeleteTodoForm, UpdateForm

app = create_app()


@app.cli.command()
def test():
    """Usa la libreria unittest para correr scripts para hacer testing
    Todos los scripts que se encuentren en la carpeta test y 
    comiencen con la palabra test serán ejecutados
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


@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    """Método que se usa para:
    - Crear una sesion y guardar la ip del usuario 
    - Crear una instancia que contiene un formulario
    Returns:
        [method]:Pasar parametros por medio de un diccionario al html y renderizar HTML 
    """
    user_ip = session.get('user_ip')
    username = current_user.id
    to_do_form = To_doForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateForm()
    context = {
        'user_ip': user_ip,
        'to_do': get_to_dos(user_id=username),
        'username': username,
        'to_do_form': to_do_form,
        'delete_form' : delete_form,
        'update_form' : update_form
    }
    if to_do_form.validate_on_submit():

        put_to_do(username, to_do_form.description.data)
        flash('Tarea creada con exito')
        return redirect(url_for('hello'))
        
    return render_template('hello.html', **context)

#Rutas dinamicas que cambian segun un parametro
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_to_do(user_id=user_id, todo_id=todo_id)
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods = ['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_to_do(user_id, todo_id, done)
    return redirect(url_for('hello'))

@app.route('/server')
def serv_error():
    raise (Exception('500 error'))
    # Es necesario apagar el modo debug para que funcione
