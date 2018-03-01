import numpy as np
from Database.errorcode import *
from Log import logger
from Database.utils import *
 
# Load Database
dbface = Load_Database_For_FaceNet()

database = {                \
    'facenet' : dbface      \
}

def get(*args):
    #First argument need to be a required database's name
    try:
        access = database
        for (i, key) in enumerate(args):
            try:
                access = access[key]
            except Exception as ex:
                raise AccessError(ex, args, key, i)
    
        return access
    except Exception as ex:
        logger.exception(ex)
        raise GetError(ex) 


def add(data, *args):
    try:
        access = get(*args)
        #Check All Key are new
        for key in data:
            if key in access:
                raise KeyConflict(key)
        #Add key and value into database
        access.update(data)

        Save_Database(database, args[0]
                )
    except Exception as ex:
        logger.exception(ex)
        raise AddError(ex)


def update(data, *args):
    try:
        access = get(*args)
        #Check All Key existed
        for key in data:
            if key not in access:
                raise KeyNotExist(key)
        #Update key and value into database
        access.update(data)

        Save_Database(database, args[0])

    except Exception as ex:
        logger.exception(ex)
        raise UpdateError(ex)


def delete(key, *args):
    try:
        access = get(*args)
        #Check if key existed
        if key not in access:
            raise KeyNotExist(key)
        #delete key permanently
        del access[key]

        Save_Database(database, args[0])

    except Exception as ex:
        logger.exception(ex)
        raise DeleteError(ex)


def clear(*args):
    try:
        access = get(*args)
        access.clear()
        
        Save_Database(database, args[0])
        
    except Exception as ex:
        logger.exception(ex)
        raise ClearError(ex)
