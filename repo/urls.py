from django.urls import path
from . import views

urlpatterns = [
    path('createrepo/', views.createRepo, name = 'craeteRepo'),
    path('<str:reponame>/createclass/', views.createClass, name = 'createClass'),
    path('<str:reponame>/<str:classname>/upload/', views.uploadedFile, name = 'uploadFile')
]
