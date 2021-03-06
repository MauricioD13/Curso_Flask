from flask import render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user, user_put
from hmac import compare_digest
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form':login_form
    }
    # Esta funcion detecta que el método es POST y que el formulario es valido,
    # cuando esto suceda entonces se ejecutará la función
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if compare_digest(password, password_from_db):
                """Se usa compare_digest porque evita los ataques de tiempos
                Es decir, no revela informacion por el tiempo de comparacion"""
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('Informacion no coicide')
        else:
            flash('Informacion no coicide')

        return redirect(url_for('index'))
    
    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }
    if signup_form.validate_on_submit():
        """Debe verificarse si ya existe ese nombre de usuario para no 
        causar problemas en la base de datos
        """
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido!')
            return redirect(url_for('hello'))
        
        else:
            flash('Usuario ya existe')

    return render_template('signup.html', **context)