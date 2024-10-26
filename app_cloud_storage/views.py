import os
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework.response import Response
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from cryptography.fernet import Fernet
from .crypto import encrypt, decrypt
import secrets

from app_cloud_storage.const import URL_SERVER
from app_cloud_storage.serializers import FilesSerializer, UsersSerializer
from .decorators import app_enter, check_session, check_status_admin
from .models import Files, UserSession, Users
import json
from django.core.exceptions import ObjectDoesNotExist

from dotenv import load_dotenv
load_dotenv()

# Create your views here.

# @api_view(['GET'])
# @ensure_csrf_cookie
# @csrf_exempt
# def get_csrf(request):
    # print('получениие токена !!!!!!!!!!!!!!!')
    # return HttpResponse()


@api_view(['POST'])
@app_enter
def registration_user(request):
    # регистрация пользователя
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(login=json_body['login'])
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

    data = user.to_json()
    data['avatar'] = f"{URL_SERVER}/media/{data['avatar']}"
    data['token'] = session.session_token
    return JsonResponse(data, status=201)

@api_view(['POST'])
@app_enter
def login_user(request):
    # вход пользователя в систему
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    queryset = Users.objects.filter(login=json_body['login'])
    if queryset.exists():
        user = queryset[0]
        if decrypt(user.password, user.key) == json_body['password']:
            data = queryset[0].to_json()
            data['avatar'] = f"{URL_SERVER}/media/{data['avatar']}"
            try:
                session = UserSession.objects.get(user_id=user.id)
                session.session_token = secrets.token_hex(16)
                session.save()
                data['token'] = session.session_token
                user.last_visit = timezone.now()
                user.save(update_fields=['last_visit'])
                return JsonResponse(data, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Нет данных по сессии. Обратитесь к администратору.'}, status=404)
        else:
            return JsonResponse({'error': 'Вы ввели неверное имя пользователя или пароль. Попробуйте повторить ввод или нажмите на кнопку регистрация.'}, status=404)
    else: 
        return JsonResponse({'error': 'Вы ввели неверное имя пользователя или пароль. Попробуйте повторить ввод или нажмите на кнопку регистрация.'}, status=404)

@api_view(['GET'])
@check_session
def logout_user(_request, data):
    # выход пользователя из системы
    data['session'].session_token = ''
    data['session'].save()
    return JsonResponse({'status': 'Выполнено'}, status=200)

@api_view(['GET'])
@check_session
def get_files(_request, data):
    # получение всех файлов пользователя
    allFiles = Files.objects.filter(user_id=data['session'].id)
    ser = FilesSerializer(allFiles, many=True)
    return Response(ser.data, status=200)

@api_view(['GET'])
@check_session
def get_data(_request, data):
    # получение данных пользователя после перезапуска (по токену)
    try:
        user = Users.objects.get(pk=data['session'].user_id.id)
        result = user.to_json()
        result['avatar'] = f"{URL_SERVER}/media/{result['avatar']}"
        result['token'] = data['session'].session_token
        return Response(result, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Нет данных на пользователя'}, status=404)
    

@api_view(['GET'])
@check_session
def file_data(_request, file_id, data):
    # получение данных о файле (обновление информации о файле у клиента)
    try:
        del data
        file = Files.objects.get(pk=file_id)
        ser = FilesSerializer(file)
        return Response(ser.data, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Файл не найден'}, status=404)

@api_view(['GET'])
@check_session
def get_link(_request, id, data):
    # формирование и отправка ссылки для скачивания файла сторонним пользователем
    try:
        title = Files.objects.get(pk=id).title
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Файл не найден'}, status=404)

    url = f"{data['session'].id}/{title}"
    key = os.getenv('URL_KEY')
    encrypt_url = encrypt(url, key)
    return JsonResponse({'url': f'{URL_SERVER}/download/{encrypt_url}'}, status=200)

@api_view(['GET'])
def download_file(_request, path):
    # скачивание файла сторонним пользователем
    try:
        key = os.getenv('URL_KEY')
        try:
            params = decrypt(path, key).split('/')
            if len(params) != 2:
                raise ObjectDoesNotExist
        except (Exception,) as err:
            raise ObjectDoesNotExist

        params = decrypt(path, key).split('/')
        file = Files.objects.get(user_id=params[0], title=params[1])
        file.last_download = timezone.now()
        file.save(update_fields=['last_download'])
        response = FileResponse(file.file, as_attachment=True, filename=params[1])
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Неверный url'}, status=404)
    except (Exception, ) as error:
        return JsonResponse({'error': f'Ошибка сервера: {error}'}, status=500)

class File(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FilesSerializer

    def post(self, request):
        # загрузка файлов на сервер (одиночное или групповое)
        @check_session
        def download(req, data):
            del data
            data_list = []
            for i in range(len(dict(req.data)['file'])):
                obj = {}
                for key, items_list in dict(req.data).items():
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

            return JsonResponse({'files': data_list}, status=201)
        return download(request)

    def get(self, request, id):
        # отправка файла для сохранения на устройство клиента
        @check_session
        def upload(_req, id, data):
            try:
                del data
                queryset = Files.objects.get(pk=id)
                queryset.last_download = timezone.now()
                queryset.save(update_fields=['last_download'])
                return FileResponse(queryset.file, as_attachment=True)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Файл не найден'}, status=404)
        return upload(request, id)

    def delete(self, request, id):
        # удаление файла из хранилища
        @check_session
        def remove(_req, id, data):
            try:
                del data
                Files.objects.get(pk=id).delete()
                return Response(status=204)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Файл не найден'}, status=404)
        return remove(request, id)

    def patch(self, request, id):
        # редактирование файла в хранилище
        @check_session
        def updata(req, id, data):
            try:
                del data
                queryset = Files.objects.get(pk=id)
                queryset.title = dict(req.data)['title'][0]
                queryset.comment = dict(req.data)['comment'][0]
                queryset.save(update_fields=['title', 'comment',])
                ser = FilesSerializer(queryset)
                return Response(ser.data, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Файл не найден'}, status=404)
        return updata(request, id)

@api_view(['GET'])
@check_session
@check_status_admin
def get_users(_request, data):
    # получение списка пользователей администратором
    allUsers = Users.objects.all()
    ser = UsersSerializer(allUsers, many=True)
    return Response(ser.data, status=200)