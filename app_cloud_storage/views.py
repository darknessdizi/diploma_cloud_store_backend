from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from app_cloud_storage.const import URL_SERVER
from app_cloud_storage.serializers import FilesSerializer
from .decorators import app_enter
from .models import Files, Users
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
def registrationUser(request):
    # регистрация пользователя
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(login=json_body['login'])
    print('****', queryset, json_body, request.headers)
    if queryset.exists():
        return HttpResponse(status=205)
    user = Users.objects.create(
        login = json_body['login'],
        full_name = json_body['fullName'],
        email = json_body['email'],
        password = json_body['password'],
    )
    print('запрос1', user.to_json())
    data = user.to_json()
    data['avatar'] = f"{URL_SERVER}/media/{data['avatar']}"
    return JsonResponse(data, status=201)

@api_view(['POST'])
@app_enter
def loginUser(request):
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
        allFiles = Files.objects.filter(user_id=id)
        ser = FilesSerializer(allFiles, many=True)
        return Response(ser.data, status=200)

    def delete(self, request, id):
        Files.objects.filter(pk=id).delete()
        return Response(status=204)