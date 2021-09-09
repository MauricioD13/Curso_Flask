from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Clase que permite usar la extension de flask WTF para el 
    uso de formularios

    Args:
        FlaskForm ([class]): Clase padre que se importa desde la extension
    """
    username = StringField('Nombre de usuario: ', validators = [DataRequired()])
    password = PasswordField('Contraseña: ', validators = [DataRequired()])
    submit = SubmitField('Enviar')

class To_doForm(FlaskForm):

    description = StringField('Descripcion', validators = [DataRequired()])
    submit = SubmitField('Crear')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateForm(FlaskForm):
    submit = SubmitField('Cambiar estado')