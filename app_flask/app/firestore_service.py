import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
#Se debe crear la credencial previamente con
#! 'gcloud auth application-default login'

firebase_admin.initialize_app(credential)

db = firestore.client()
#Comunicacion con la base de datos

def get_users():
    """
    Trae todos los usuarios a de la base de datos
    """
    return db.collection('users').get()

def get_user(user_id):
    """
    Trae el usuario dado por el user_id
    """
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({
        'password': user_data.password
    })

def get_to_dos(user_id):
    """
    En la coleccion de usuarios se busca en el documento del usuario
    en cuestion y se trae la coleccion de to dos
    """
    return db.collection('users')\
        .document(user_id)\
        .collection('to-dos').get()

def put_to_do(user_id, description):

    to_dos_collection_ref = db.collection('users')\
        .document(user_id).collection('to-dos')
    to_dos_collection_ref.add({
        'description': description,
        'done' : False
    })

def delete_to_do(user_id, todo_id):
    #todo_ref = db.collection('users')\
    #        .document(user_id).collection('to-dos')\
    #        .document(todo_id)

    #Forma alternativa

    todo_ref = __get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_to_do(user_id, todo_id, done):
    todo_ref = __get_todo_ref(user_id, todo_id)
    todo_ref.update({
        'done': not bool(done)
    })

def __get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/to-dos/{todo_id}')