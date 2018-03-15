from django.urls import path
from . import views

urlpatterns = [
    path('create_repo/', views.create_repo, name='create_repo'),
    path('<str:repo_name>/create_class/', views.create_class, name='create_class'),
    path('<str:repo_name>/<str:class_name>/upload/', views.uploadedFile, name='uploadFile')
]
