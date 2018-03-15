from django.urls import path
from . import views

urlpatterns = [
    path('recognize/', views.rec_list, name='recList'),
    path('train/', views.train, name='train'),
]
