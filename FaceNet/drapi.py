from Database import database as db

def Load_FaceNet_Database():
    return db.get('facenet')

def Add_New_Encoding(label, encode):
    db.add({label : encode}, 'facenet')
<<<<<<< 869b351157246f70e32660a092aa83d6b95adf57
    
=======

def Del_Sample(label):
    db.delete(label, 'facenet')

def Clear_Database():
    db.clear('facenet')
>>>>>>> Initialize new branch
