from django.urls import path
from . import views

urlpatterns = [
    path('<str:repo_name>/', views.rec_list, name='recList')
]
