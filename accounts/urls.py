from django.urls import path
from rest_framework.authtoken import views as rest_framework_views
from . import views as local_views

urlpatterns = [
    path('get_auth_token/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    path('register/', local_views.register, name='register'),
]
