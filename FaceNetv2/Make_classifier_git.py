from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
from FaceNetv2 import facenet
from FaceNetv2 import  detect_face
import os
import sys
import math
import pickle
from sklearn.svm import SVC


def getNewPaths(old_paths, tpaths, tlabels):
    paths = []
    labels = []
    for (i, path) in enumerate(tpaths):
        label = tlabels[i]
        if path in old_paths:
            old_paths[path] = label
            continue
        paths.append(path)
        labels.append(label)
        old_paths[path] = label

    return np.array(paths), np.array(labels), old_paths

def getLabels(new_paths, paths):
    labels = []
    print('New paths and labels:')
    for path in paths:
        label = new_paths[path]
        print(' {} - {}'.format(path, label))
        labels.append(label)
    return labels

def run():

    with tf.Graph().as_default():

        with tf.Session() as sess:

            old_paths = {}
            if os.path.exists('FaceNetv2/output_dir/old_paths.npy'):
                old_paths = np.load('FaceNetv2/output_dir/old_paths.npy').item()
                print("old_paths type: {}".format(type(old_paths)))

            datadir = 'FaceNetv2/output_dir/'
            dataset = facenet.get_dataset(datadir)
            tpaths, tlabels = facenet.get_image_paths_and_labels(dataset)

            paths, labels, new_paths = getNewPaths(old_paths, tpaths, tlabels)

            print('Number of classes: %d' % len(dataset))
            print('Number of images: %d' % len(paths))

            print('Loading feature extraction model')
            modeldir = 'FaceNetv2/20170511-185253/20170511-185253.pb'
            facenet.load_model(modeldir)

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            # Run forward pass to calculate embeddings
            print('Calculating features for images')
            batch_size = 1000
            image_size = 160
            nrof_images = len(paths)
            nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
            emb_array = np.zeros((nrof_images, embedding_size))
            for i in range(nrof_batches_per_epoch):
                start_index = i * batch_size
                end_index = min((i + 1) * batch_size, nrof_images)
                paths_batch = paths[start_index:end_index]
                images = facenet.load_data(paths_batch, False, False, image_size)
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)

            classifier_filename = 'FaceNetv2/my_classifier.pkl'
            classifier_filename_exp = os.path.expanduser(classifier_filename)


            if os.path.exists('FaceNetv2/output_dir/old_emb_array.npy'):
                old_emb_array = np.load('FaceNetv2/output_dir/old_emb_array.npy')
                old_paths_arr = np.load('FaceNetv2/output_dir/old_paths_arr.npy')
                emb_array = np.concatenate((emb_array, old_emb_array))
                paths = np.concatenate((paths, old_paths_arr))
                labels = getLabels(new_paths, paths)

            # Train classifier
            print('Training classifier')
            model = SVC(kernel='linear', probability=True)
            model.fit(emb_array, labels)

            # Create a list of class names
            class_names = [cls.name.replace('_', ' ') for cls in dataset]

            # Saving classifier model
            with open(classifier_filename_exp, 'wb') as outfile:
                pickle.dump((model, class_names), outfile)
            
            np.save('FaceNetv2/output_dir/old_paths.npy', new_paths)
            np.save('FaceNetv2/output_dir/old_emb_array.npy', emb_array)
            np.save('FaceNetv2/output_dir/old_paths_arr.npy', paths)

            print('Saved classifier model to file "%s"' % classifier_filename_exp)
            print('Goodluck')