from Database import database as db

def Load_FaceNet_Database():
    return db.get('facenet')

