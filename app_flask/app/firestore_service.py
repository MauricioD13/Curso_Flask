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

def get_to_dos(user_id):
    """

    """
    return db.collection('users')\
        .document(user_id)\
        .collection('to-dos').get()
