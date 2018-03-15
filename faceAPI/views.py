from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE
import shlex
import json
#from FaceNet import face_recognition as fr
from FaceNetv2 import face_recognition as fr
import numpy as np
import cv2

baseurl = 'FaceDetect/bin/'
cmd = './' + baseurl + 'darknet detector test ' + baseurl + 'yolo-face.names ' + baseurl + 'yolo-face-test.cfg ' + baseurl + 'yolo-face.weights -thresh 0.24 stream crop'

def getImageFromByteStream(img_str):
    print('Length of the byte stream: ' + str(len(img_str)))
    nparr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def getImageBoxes(img_str):

    img = getImageFromByteStream(img_str)

    print ('Passing the byte stream directly to FaceDetect API...')
    proc = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    outputs, errs = proc.communicate(input=img_str)
    print('FaceDetect returns results: ' + str(outputs))
    # Convert byte result into lists of box
    boxes = [[int(e) for e in x] for x in [s.split(' ') for s in str(outputs)[2:-1].split('\\n')[:-1]]]
    print('Converted boxes: ' + str(boxes))
    
    return img, boxes

def getHttpReponseFromFaceResults(labels, boxes):
    tempres = [0, labels, boxes]

    if tempres[0] != 0:
        return httpresponse('fail')
    else:
        code, labels, bounding_boxs = tempres
        res = dict()
        res['results'] = []
        for i in range(labels.__len__()):
            res['results'].append({"name": labels[i], "boundingbox": bounding_boxs[i]})
        res = json.dumps(res)
    return HttpResponse(res)


def serverCall(content):
    if type(content).__name__ == "InMemoryUploadedFile":

        img_str = content.read()
        
        img, boxes = getImageBoxes(img_str)

        print('Passing image and boxes into FaceNet API...')
        results = fr.recognize(img, boxes)
        print('Recognize: ' + str(results))

        if len(results) > 0:
            labels = np.array(results)[:,1]
        else:
            labels = []

        return getHttpReponseFromFaceResults(labels, boxes)

    else:

        print('Not implemented this feature')

        return [1]

def addSampleCall(label, image):
    img_str = image.read()

    img, boxes = getImageBoxes(img_str)
    
    if len(boxes) == 0:
        boxes.append([0, 0, img.shape[1]-1, img.shape[0] - 1])

    print('Passing label, image and boxes into FaceNet API...')
    fr.addsample(label, img, boxes)
    print('Add sample finished')
    
    return HttpResponse()


def facenetv2_serverCall(content):
    if type(content).__name__ == "InMemoryUploadedFile":

        img_str = content.read()
       
        img = getImageFromByteStream(img_str)

        labels, boxes = fr.recognize(img)

        print(labels, boxes)

        return getHttpReponseFromFaceResults(labels, boxes.tolist()) 

    else:

        print('Not implemented this feature')

        return [1]

def facenetv2_train(media):
    filezip = media.read()
    fr.train(filezip)

    

@csrf_exempt
def rec_list(request):
    if request.method == 'POST':
        img = request.FILES['image']
        response = facenetv2_serverCall(img)
        return HttpResponse(response)
    else:
        return HttpResponse("fail")

@csrf_exempt
def addsample(request):
    if request.method == 'POST':
        img = request.FILES['image']
        label = request.POST['label']
        response = addSampleCall(label, img)
        return HttpResponse(response)
    else:
        return HttpResponse('fail')

@csrf_exempt
def train(request):
    if request.method == 'POST':
        filezip = request.FILES['train_data']
        response = facenetv2_train(filezip)
        return HttpResponse(response)
    else:
        return HttpResponse('fail')

# Create your views here.
