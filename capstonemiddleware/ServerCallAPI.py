import requests
import json
import re

urlpattern = re.compile('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
serverURL = 'http://188.166.244.173:8000/recognise' 

def request(image):
    assert(type(image).__name__ == 'InMemoryUploadedFile'
           or type(image).__name__ == 'str' and urlpattern.match(image))
    if type(image).__name__ == 'InMemoryUploadedFile':
        r = requests.post(serverURL, files={'image':image})
    else:
        r = requests.get(serverURL + '?url=' + image)
    data = json.loads(r.text)
    if data['code'] == 0:
        labels = data['names']
        bounding_boxes = data['coordinates']
        for (i, bounding_box) in enumerate(bounding_boxes):
            bounding_boxes[i] = json.loads('[' + bounding_box + ']')
        return [data['code'], labels, bounding_boxes]
    return [data['code']]
