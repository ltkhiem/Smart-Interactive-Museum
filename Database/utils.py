import numpy as np

def Load_Database_For_FaceNet():
    dbface_filename = 'facenet.npy'
    dbface = np.load('Database/' + dbface_filename).item()
    return dbface

def Save_Database(db, dbname):
    np.save('Database/' + dbname + '.npy', db[dbname])
    
