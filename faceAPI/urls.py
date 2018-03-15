from django.urls import path
from . import views

urlpatterns = [
	path('train/', views.train, name='train'),
    path('recognize/', views.rec_list, name='recList'),
    path('addsample/', views.addsample, name='addsample'),
]
