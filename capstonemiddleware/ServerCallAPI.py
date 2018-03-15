import json
import re

import requests

urlpattern = re.compile('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
external_API = False 
serverAnhAnURL = 'http://188.166.244.173:8000/'
serverTienURL = 'http://104.199.208.75/'
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

def requestTien(content):
    serverTienRecognize = serverTienURL + 'recognize/'
    if type(content).__name__ == 'InMemoryUploadedFile':
        r = requests.post(serverTienRecognize, files={'image':content})
    else:
        r = requests.get(serverTienRecognize + '?url=' + content)
    data = json.loads(r.text)
    print(data)
    return data

def trainTien(content):
    img = content.FILES['img']
    label = content.POST['label']
    serverTienTrain = serverTienURL + 'addsample/'
    if type(img).__name__ == 'InMemoryUploadedFile':
        r = requests.post(serverTienTrain, files={'image':img}, data={'label': label})
    else:
        r = requests.get(serverTienTrain + '?url=' + img)
    data = r.text
    return data


