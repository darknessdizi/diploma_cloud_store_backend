from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .decorators import app_enter
from .models import Files, Users
import json

# Create your views here.

@csrf_exempt
# @api_view(['POST'])
@app_enter
def registrationUser(request):
    # регистрация пользователя
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(user_login=json_body['login'])
    print('****', queryset, json_body)
    if queryset.exists():
        return HttpResponse(status=205)
    user = Users.objects.create(
        user_login = json_body['login'],
        user_full_name = json_body['fullName'],
        user_email = json_body['email'],
        user_password = json_body['password'],
    )
    print('запрос1', user.to_json())
    return JsonResponse(user.to_json(), status=201)

@csrf_exempt
# @api_view(['POST'])
@app_enter
def loginUser(request):
    # вход пользователя в систему
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(user_login=json_body['login'], user_password=json_body['password'])
    if queryset.exists():
        return JsonResponse(queryset[0].to_json(), status=200)    
    else: 
        return HttpResponse(status=205)
