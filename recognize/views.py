import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from capstonemiddleware import ServerCallAPI

# Create your views here.

@csrf_exempt
def rec_list(request):
    if request.method == 'POST':
        img = request.FILES['img']
        response = ServerCallAPI.request(img)
        if response[0] != 0:
            return HttpResponse('fail')
        else:
            code, labels, bounding_boxs = response
            res = dict()
            res['results'] = []
            for i in range(labels.__len__()):
                res['results'].append({"name": labels[i], "boundingbox": bounding_boxs[i]})
            res = json.dumps(res)
        return HttpResponse(res)
    else:
        return HttpResponse("fail")
