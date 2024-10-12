from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from cryptography.fernet import Fernet
from .crypto import encrypt, decrypt
import secrets

from app_cloud_storage.const import URL_SERVER
from app_cloud_storage.serializers import FilesSerializer
from .decorators import app_enter
from .models import Files, UserSession, Users
import json

# Create your views here.

@api_view(['GET'])
@ensure_csrf_cookie
@csrf_exempt
def get_csrf(request):
    print('получениие токена !!!!!!!!!!!!!!!')
    return HttpResponse()

@api_view(['POST'])
@app_enter
def registration_user(request):
    # регистрация пользователя
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(login=json_body['login'])
    # print('****', queryset, json_body, request.headers)
    if queryset.exists():
        return HttpResponse(status=205)

    if json_body['sex'] == 'man':
        avatar_name = 'avatar-man.svg'
    else:
        avatar_name = 'avatar-woman.svg'

    key = Fernet.generate_key().decode()
    user = Users.objects.create(
        login = json_body['login'],
        full_name = json_body['fullName'],
        email = json_body['email'],
        password = encrypt(json_body['password'], key),
        sex = json_body['sex'],
        avatar = avatar_name,
        key = key,
    )

    session = UserSession.objects.create(
        user_id = user,
        session_token = secrets.token_hex(16),
    )

    print('запрос1', user.to_json())
    data = user.to_json()
    data['avatar'] = f"{URL_SERVER}/media/{data['avatar']}"
    data['session_token'] = session.session_token
    return JsonResponse(data, status=201)

@api_view(['POST'])
@app_enter
def login_user(request):
    # вход пользователя в систему
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(login=json_body['login'], password=json_body['password'])
    if queryset.exists():
        data = queryset[0].to_json()
        data['avatar'] = f"{URL_SERVER}/media/{data['avatar']}"
        return JsonResponse(data, status=200)    
    else: 
        return HttpResponse(status=205)

@api_view(['GET'])
@app_enter
def get_files(request, id):
    # получение всех файлов пользователя
    allFiles = Files.objects.filter(user_id=id)
    ser = FilesSerializer(allFiles, many=True)
    return Response(ser.data, status=200)

@api_view(['GET'])
@app_enter
def file_data(request, file_id):
    # получение данных о файле
    file = Files.objects.get(pk=file_id)
    ser = FilesSerializer(file)
    return Response(ser.data, status=200)   

class File(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FilesSerializer

    def post(self, request):
        # загрузка файлов на сервер (одиночное или групповое)
        data_list = []
        for i in range(len(dict(request.data)['file'])):
            obj = {}
            for key, items_list in dict(request.data).items():
                obj[key] = items_list[i]

            serializer = self.serializer_class(data=obj)
            if serializer.is_valid():
                serializer.save()
                data_list.append({
                    'id': serializer.data['id'],
                    'title': serializer.data['title'],
                    'comment': serializer.data['comment'],
                    'size': serializer.data['size'],
                    'created': serializer.data['created'],
                    'last_download': serializer.data['last_download'],
                })

        return Response(data={'files': data_list}, status=201)

    def get(self, request, id):
        # отправка файла для сохранения на устройство клиента
        print('отправка файла', id)
        queryset = Files.objects.get(pk=id)
        queryset.last_download = timezone.now()
        queryset.save(update_fields=['last_download'])
        return FileResponse(queryset.file, as_attachment=True) 

    def delete(self, request, id):
        # удаление файла из хранилища
        Files.objects.filter(pk=id).delete()
        return Response(status=204)