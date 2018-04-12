import json
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from capstonemiddleware import ServerCallAPI


# Create your views here.

# @csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def rec_list(request, repo_name):
    if request.method == 'POST':
        img = request.FILES['img']
        server = request.POST['server']
        if (server == 'anhAn'):
            response = ServerCallAPI.requestAnhAn(img)
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
        elif server == 'tien':
            response = ServerCallAPI.requestTien(repo_name, img)
            return HttpResponse(str(response))
        elif server == 'tu':
            response = ServerCallAPI.requestTu(repo_name, img)
            return HttpResponse(str(response))
        else:
            print("not an valid server")
            raise Exception
    else:
        return HttpResponse("fail")
