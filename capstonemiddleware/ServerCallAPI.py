import json
import re
from capstonemiddleware.settings import serverAnhAnURL, serverTienURL, serverTuURL

import requests

urlpattern = re.compile('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
external_API = False 
serverAnhAnURL = 'http://188.166.244.173:8000/'
serverTienURL = 'http://104.199.208.75/'
serverTuURL = 'http://35.201.166.3/'
baseurl = 'FaceDetect/bin/'
cmd = './' + baseurl + 'darknet detector test ' + baseurl + 'yolo-face.names ' + baseurl + 'yolo-face-test.cfg ' + baseurl + 'yolo-face.weights -thresh 0.24 stream crop'
maxFileSize = 5 * 2 ** 20

def requestAnhAn(content):
    # Check type of the request content and the size of it must be valid
    assert(type(content).__name__ == 'InMemoryUploadedFile' and content.size < maxFileSize
           or type(content).__name__ == 'str' and urlpattern.match(content))

    if type(content).__name__ == 'InMemoryUploadedFile':
        r = requests.post(serverAnhAnURL, files={'image':content})
    else:
        r = requests.get(serverAnhAnURL + '?url=' + content)

    data = json.loads(r.text)

    if data['code'] == 0:
        labels = data['names']
        bounding_boxes = data['coordinates']

        for (i, bounding_box) in enumerate(bounding_boxes):
            bounding_boxes[i] = json.loads('[' + bounding_box + ']')

        return [data['code'], labels, bounding_boxes]

    return [data['code']]

def requestTien(img):
    serverTienRecognize = serverTienURL + 'recognize/'
    r = requests.post(serverTienRecognize, files={'image':img})
    data = json.loads(r.text)
    print(data)
    return data

def trainTien(zipfile):
    serverTienTrain =serverTienURL + 'train/'
    r = requests.post(serverTienTrain, files={'train_data':zipfile})
    return r.text

def trainTu(zipdata, token):
    serverTuTrain = serverTuURL + 'train/'
    print(zipdata, token)
    r = requests.post(serverTuTrain, files={'data':zipdata}, data={'token':token})
    return r.text

def requestTu(repo_name, token, img):
    serverTuRecognize = serverTuURL + 'test/' + repo_name + '/'
    r = requests.post(serverTuRecognize, files={'img':img}, data={'token':token})
    result = json.load(r.text)
    return result

def demoTu(img, token):
    serverTuRecognize = serverTuURL + 'demo' + '/'
    r = requests.post(serverTuRecognize, files={'img':img}, data={'token':token})
    print(r.text)
    return r.text

