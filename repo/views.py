import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from capstonemiddleware.settings import REPO_URL
from repo.models import Repo
from repo.permissions import IsOwner
from repo.serializers import RepoSerializer, ClassSerializer


# Create your views here.

# class CreateRepoView(generics.ListCreateAPIView):
#     queryset = Repo.objects.all()
#     serializer_class = RepoSerializer
#     permission_classes = (IsAuthenticated, IsOwner,)
#
#     def perform_create(self, serializer):
#         serializer.save()


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_repo(request):
    if request.method == 'GET':
        return HttpResponse("fail")
    serializer = RepoSerializer(data=request.data)
    if serializer.is_valid():
        repo_name = request.POST['name']
        new_repo_url = REPO_URL + repo_name
        if os.path.isdir(new_repo_url):
            return HttpResponse("this repo has already occupied")
        os.makedirs(new_repo_url)
        serializer.save(owner=request.user)
        return HttpResponse("create repo " + repo_name + " successfully")
    return HttpResponse("fail")


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_class(request, repo_name):
    if request.method == 'GET':
        return HttpResponse("fail")
    serializer = ClassSerializer(data=request.data)
    if serializer.is_valid():
        repo = Repo.objects.get(name=repo_name)
        serializer.save(repo=repo)
        new_repo_url = REPO_URL + repo_name + '/'
        if not os.path.isdir(new_repo_url):
            return HttpResponse("this repo doesn't exist")
        class_name = request.POST['name']
        new_class_url = new_repo_url + class_name + '/'
        if os.path.isdir(new_class_url):
            return HttpResponse("this class has already occupied")
        os.makedirs(new_class_url)
        return HttpResponse("create class " + class_name + " successfully")
    return HttpResponse("fail")


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def uploadedFile(request, reponame, classname):
    if request.method == 'GET':
        return HttpResponse("fail")
    newRepoUrl = REPO_URL + reponame + '/'
    if not os.path.isdir(newRepoUrl):
        return HttpResponse("this repo doesn't exist")
    secret = request.POST['secret']
    with open(newRepoUrl + '/secret.txt', 'r') as f:
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
            for each in t.chunks():  # request.FILES['img'].chunks():
                f.write(each)
    #     print(each)
    #     print('zzz')
    # image = Image.open(io.BytesIO(each))
    # image.save(newClassUrl + 'aa', 'PNG')
    return HttpResponse("success")
