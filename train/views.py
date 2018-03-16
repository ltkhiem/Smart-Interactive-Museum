from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from capstonemiddleware import ServerCallAPI


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def train_image(request):
    if request.method == 'GET':
        return HttpResponse('fail')

    if request.POST['server'] == 'tien':
        response = ServerCallAPI.trainTien(request)
        return HttpResponse(str(response))
    else:
        return HttpResponse('fail')
