from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from scipy import misc
import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse
from FaceNetv2 import facenet
from FaceNetv2 import detect_face
import os
from os.path import join as pjoin
import sys
import time
import copy
import math
import pickle
from sklearn.svm import SVC
from sklearn.externals import joblib
from Log import logger
import zipfile
import FaceNetv2.Make_aligndata_git as make_aligndata
import FaceNetv2.Make_classifier_git as make_classifier

if not os.path.isdir('FaceNetv2/20170511-185253'):
    logger.info('Downloading model...')
    import FaceNetv2.download_model
    logger.info('Downloading completed!')

if not os.path.isfile('FaceNetv2/my_classifier.pkl'):
    logger.info('Preprocessing data...')
    make_aligndata.run()
    make_classifier.run()
    logger.info('Preprocessing data completed!')


minsize = 20  # minimum size of face
threshold = [0.6, 0.7, 0.7]  # three steps's threshold
factor = 0.709  # scale factor
image_size = 182
input_image_size = 160


logger.info('Creating networks and loading parameters')
with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, 'FaceNetv2/')


        print('Loading feature extraction model')
        modeldir = 'FaceNetv2/20170511-185253/20170511-185253.pb'
        facenet.load_model(modeldir)

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]


def load():
    global HumanNames, model
    HumanNames = sorted(os.listdir('FaceNetv2/data'))    #train human name

    print('Human Names: {}'.format(HumanNames))

    classifier_filename = 'FaceNetv2/my_classifier.pkl'
    classifier_filename_exp = os.path.expanduser(classifier_filename)
    with open(classifier_filename_exp, 'rb') as infile:
        (model, class_names) = pickle.load(infile)
    print('load classifier file-> %s' % classifier_filename_exp)

load()

logger.info('loading model completed!')

def recognize(frame):
    #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)

    if frame.ndim == 2:
        frame = facenet.to_rgb(frame)
    frame = frame[:, :, 0:3]
    bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]
    print('Detected_FaceNum: %d' % nrof_faces)

    if nrof_faces > 0:
        det = bounding_boxes[:, 0:4]
        img_size = np.asarray(frame.shape)[0:2]

        cropped = []
        scaled = []
        scaled_reshape = []
        bb = np.zeros((nrof_faces,4), dtype=np.int32)

        result_names = []

        for i in range(nrof_faces):
            emb_array = np.zeros((1, embedding_size))

            bb[i][0] = det[i][0]
            bb[i][1] = det[i][1]
            bb[i][2] = det[i][2]
            bb[i][3] = det[i][3]

            # inner exception
            if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                print('face is inner of range!')
                continue

            cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
            cropped[0] = facenet.flip(cropped[0], False)
            scaled.append(misc.imresize(cropped[0], (image_size, image_size), interp='bilinear'))
            scaled[0] = cv2.resize(scaled[0], (input_image_size,input_image_size),
                                   interpolation=cv2.INTER_CUBIC)
            scaled[0] = facenet.prewhiten(scaled[0])
            scaled_reshape.append(scaled[0].reshape(-1,input_image_size,input_image_size,3))
            feed_dict = {images_placeholder: scaled_reshape[0], phase_train_placeholder: False}
            emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
            predictions = model.predict_proba(emb_array)
            best_class_indices = np.argmax(predictions, axis=1)
            best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

            print('result index: ', best_class_indices[0])
            result_name = HumanNames[best_class_indices[0]]

            result_names.append(result_name)

        return (result_names, bb)
    else:
        print('Unable to align')

    return ([], np.array([]))


def train(filezip):
    with open('train_data.zip', 'wb') as f:
        f.write(filezip)

    logger.info('Extracting train data...')
    zip_ref = zipfile.ZipFile('train_data.zip', 'r')
    zip_ref.extractall('FaceNetv2/data')
    zip_ref.close()
    os.remove('train_data.zip')
    logger.info('Extracting train data completed!')

    logger.info('Training...')
    make_aligndata.run()
    make_classifier.run()
    load()
    logger.info('Training completed!')



#test_dir = 'test/'
#for test_image_name in os.listdir(test_dir):
    # test_image_file = os.path.join(test_dir, test_image_name)

    # test_image = cv2.imread(test_image_file)

    # res = recognize(test_image)

    # print("image name {}: {}".format(test_image_name, res))