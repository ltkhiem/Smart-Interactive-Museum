import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from capstonemiddleware import ServerCallAPI

# Create your views here.

@csrf_exempt
def recList(request):
    if (request.method == 'POST'):
        img = request.FILES['img']
        response = ServerCallAPI.request(img)
        if response[0] != 0:
            return HttpResponse('fail')
        else:
            code, labels, bounding_boxs = response
            print(bounding_boxs)
            res = {}
            res['results'] = []
            for i in range(labels.__len__()):
                res['results'].append({"name": labels[i], "boundingbox": bounding_boxs[i]})
            # res = {'results': [{"name": "chocam", "boundingbox": [1, 2, 3, 4]}, {"name": "chokhiem", "boundingbox": [5, 6, 7, 8]}]}
            res = json.dumps(res)
        return HttpResponse(res)
    else:
        return HttpResponse("fail")