from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from capstonemiddleware.settings import REPO_URL

from capstonemiddleware import ServerCallAPI
from capstonemiddleware.utils import zipdir


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def train_image(request):
    if request.method == 'GET':
        return HttpResponse('fail')

    if request.POST['server'] == 'tien':
        response = ServerCallAPI.trainTien(request)
        return HttpResponse(str(response))
    elif request.POST['server'] == 'tu':
        response = ServerCallAPI.trainTu(request.FILES['data'])
        return HttpResponse(str(response))
    else:
        return HttpResponse('fail')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def train_repo(request, repo_name):
    newRepoUrl = REPO_URL + repo_name + '/'
    zipfile = zipdir(newRepoUrl, repo_name)
    res = ServerCallAPI.trainTu(zipfile, request.META['Authorization'][6:])
    return HttpResponse(res)
