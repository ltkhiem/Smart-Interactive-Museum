from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.demo, name='demo'),
    path('everything/', views.rec_everything, name='recEvery'),
    path('<str:repo_name>/', views.rec_list, name='recList')
]
