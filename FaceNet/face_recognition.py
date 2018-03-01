from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
K.set_image_data_format('channels_first')
import numpy as np
from numpy import genfromtxt
import tensorflow as tf
from FaceNet.fr_utils import *
from FaceNet.inception_block import *
from Log import logger
from FaceNet.drapi import *

FRmodel = faceRecoModel(input_shape=(3, 96, 96)) # Total params ~ 3.75 millions

def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    # Step 1: Compute the (encoding) distance between the anchor and the positive, you will need to sum over axis=-1
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis = -1)
    # Step 2: Compute the (encoding) distance between the anchor and the negative, you will need to sum over axis=-1
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis = -1)
    # Step 3: subtract the two previous distances and add alpha.
    basic_loss = pos_dist - neg_dist + alpha
    # Step 4: Take the maximum of basic_loss and 0.0. Sum over the training examples.
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0)) 
    
    return loss

# Loading the trained model

FRmodel.compile(optimizer = 'adam', loss = triplet_loss, metrics = ['accuracy'])
logger.info('Loading Weights')
load_weights_from_FaceNet(FRmodel)
logger.info('Loading Weights Completed')

#Face Verification
def verify(img, identity, database, model):
    # Step 1: Compute the encoding for the image. Use img_to_encoding() see example above. (≈ 1 line)
    encoding = img_to_encoding(img, model)

    # Step 2: Compute distance with identity's image (≈ 1 line)
    dist = np.linalg.norm(database[identity] - encoding)
    
    accept = dist < 0.7

    return dist, accept

def recognize_single(img, database, model):
    ## Step 1: Compute the target "encoding" for the image. Use img_to_encoding() see example above. ## (≈ 1 line)
    encoding = img_to_encoding(img, model)
    
    ## Step 2: Find the closest encoding ##
    
    # Initialize "min_dist" to a large value, say 100 (≈1 line)
    min_dist = 100
    
    # Loop over the database dictionary's names and encodings.
    for (name, db_enc) in database.items():
        
        # Compute L2 distance between the target "encoding" and the current "emb" from the database. (≈ 1 line)
        dist = np.linalg.norm(db_enc - encoding)
        
        print('\tdistance to "%s" is %f' % (name, dist))

        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. (≈ 3 lines)
        if min_dist > dist:
            min_dist = dist
            identity = name

    ### END CODE HERE ###
    return min_dist, identity

def recognize(img, boxes):

    database = Load_FaceNet_Database()

    results = []

    for (i, box) in enumerate(boxes):
        print('Processing box [%d %d %d %d]' % tuple(box)) 
        left, top, right, bot = box
        crop_img = img[top:bot+1, left:right+1]

        # resize image to match the require size of the input layer
        resized_img = cv2.resize(crop_img, (96, 96))
        
        min_dist, identity = recognize_single(resized_img, database, FRmodel)
        
        if min_dist < 0.7:
            results.append((min_dist, identity))
        else:
            results.append((min_dist, 'unknown'))
    
    return results
