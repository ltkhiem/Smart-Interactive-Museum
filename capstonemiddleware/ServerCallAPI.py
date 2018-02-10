import requests
import json
import re
from subprocess import Popen, PIPE
import shlex
import numpy as np

urlpattern = re.compile('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
external_API = False 
serverURL = 'http://188.166.244.173:8000/recognise' 
baseurl = 'FaceDetect/bin/'
cmd = './' + baseurl + 'darknet detector test ' + baseurl + 'yolo-face.names ' + baseurl + 'yolo-face-test.cfg ' + baseurl + 'yolo-face.weights -thresh 0.24 stream crop'
maxFileSize = 5 * 2 ** 20

if not external_API:
    from FaceNet import face_recognition as fr
    

def request(content):
    # Check type of the request content and the size of it must be valid
    assert(type(content).__name__ == 'InMemoryUploadedFile' and content.size < maxFileSize
           or type(content).__name__ == 'str' and urlpattern.match(content))

    if external_API:

        if type(content).__name__ == 'InMemoryUploadedFile':
            r = requests.post(serverURL, files={'image':content})
        else:
            r = requests.get(serverURL + '?url=' + content)

        data = json.loads(r.text)

        if data['code'] == 0:
            labels = data['names']
            bounding_boxes = data['coordinates']

            for (i, bounding_box) in enumerate(bounding_boxes):
                bounding_boxes[i] = json.loads('[' + bounding_box + ']')

            return [data['code'], labels, bounding_boxes]

        return [data['code']]

    else:
        if type(content).__name__ == "InMemoryUploadedFile":

            img_str = content.read()
            print('Length of the byte stream: ' + str(len(img_str)))
        
            import numpy as np
            import cv2
            # Convert to image for passing through FaceNet API
            nparr = np.fromstring(img_str, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            print ('Passing the byte stream directly to FaceDetect API...')
            proc = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
            outputs, errs = proc.communicate(input=img_str)
            print('FaceDetect returns results: ' + str(outputs))
            # Convert byte result into lists of box
            boxes = [[int(e) for e in x] for x in [s.split(' ') for s in str(outputs)[2:-1].split('\\n')[:-1]]] 
            print('Converted boxes: ' + str(boxes))
            
            print('Passing image and boxes into FaceNet API...')
            results = fr.recognize(img, boxes, fr.database, fr.FRmodel)
            print('Recognize: ' + str(results))
            
            if len(results) > 0:
                labels = np.array(results)[:,1]
            else:
                labels = []
            
            return [0, labels, boxes]
        
        else:
            
            print('Not implemented this feature')

            return [1] 


  
