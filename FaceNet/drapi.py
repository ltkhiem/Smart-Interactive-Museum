from Database import database as db

def Load_FaceNet_Database():
    return db.get('facenet')

def Add_New_Encoding(label, encode):
    db.add({label : encode}, 'facenet')
    
