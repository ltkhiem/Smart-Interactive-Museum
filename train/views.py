from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from capstonemiddleware import ServerCallAPI

@csrf_exempt
def train_image(request):
    if request.method == 'GET':
        return HttpResponse('fail')

    if request.POST['server'] == 'tien':
        response = ServerCallAPI.trainTien(request)
        return HttpResponse(str(response))
    else:
        return HttpResponse('fail')
