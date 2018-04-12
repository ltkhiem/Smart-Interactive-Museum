from django.urls import path
from . import views

urlpatterns = [
    path('', views.train_image, name='trainImage'),
    path('repo/<str:repo_name>/', views.train_repo, name='trainRepo')
]
