from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


@csrf_exempt
def register(request):
    res = dict()
    if request.method == "POST":
        res['success'] = False
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    res['token'] = str(token)
                    res['success'] = True
        else:
            res['error'] = str(form.errors)
    else:
        res['error'] = "Only accept POST request"
    res = json.dumps(res)
    return HttpResponse(res)
