import os
import sys
import io
from .forms import *

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView, View
from PIL import Image

from capstonemiddleware.settings import REPO_URL, IMAGE_NAME

# Create your views here.

@csrf_exempt
def createRepo(request):
    if (request.method == 'GET'):
        return HttpResponse("fail")
    repoName = request.POST['reponame']
    newRepoUrl = REPO_URL+repoName
    secret = request.POST['secret']
    if (os.path.isdir(newRepoUrl)):
        return HttpResponse("this repo has already occupied")
    os.makedirs(newRepoUrl)
    print(newRepoUrl)
    with open(newRepoUrl + '/secret.txt', 'w') as f:
        f.write(secret)
    return HttpResponse("create repo " + repoName + " successfully")

@csrf_exempt
def createClass(request, reponame):
    if request.method == 'GET':
        return HttpResponse("fail")
    newRepoUrl = REPO_URL + reponame + '/'
    if not os.path.isdir(newRepoUrl):
        return HttpResponse("this repo doesn't exist")
    className = request.POST['classname']
    secret = request.POST['secret']
    with open(newRepoUrl + '/secret.txt', 'r' ) as f:
        realSecret = f.read()
    if secret != realSecret:
        return HttpResponse("secret is not true")
    newClassUrl = newRepoUrl + className + '/'
    if os.path.isdir(newClassUrl):
        return HttpResponse("this class has already occupied")
    os.makedirs(newClassUrl)
    return HttpResponse("create class " + className + " successfully")

@csrf_exempt
def uploadedFile(request, reponame, classname):
    if request.method == 'GET':
        return HttpResponse("fail")
    newRepoUrl = REPO_URL + reponame + '/'
    if not os.path.isdir(newRepoUrl):
        return HttpResponse("this repo doesn't exist")
    secret = request.POST['secret']
    with open(newRepoUrl + '/secret.txt', 'r' ) as f:
        realSecret = f.read()
    if secret != realSecret:
        return HttpResponse("secret is not true")
    newClassUrl = newRepoUrl + classname + '/'
    if not os.path.isdir(newClassUrl):
        return HttpResponse("this class hasn't exist")
    # print(type(request.FILES['img'].chunk))
    global IMAGE_NAME
    for t in request.FILES.getlist('img'):
        IMAGE_NAME += 1
        with open(newClassUrl + str(IMAGE_NAME) + '.png', 'wb+') as f:
            for each in t.chunks(): #request.FILES['img'].chunks():
                f.write(each)
    #     print(each)
    #     print('zzz')
        # image = Image.open(io.BytesIO(each))
        # image.save(newClassUrl + 'aa', 'PNG')
    return HttpResponse("success")

