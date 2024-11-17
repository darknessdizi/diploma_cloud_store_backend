import logging
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app_cloud_storage.models import UserSession

logger = logging.getLogger(__name__)


# Декоратор для входа в систему
def app_enter(func):
    def wrapped(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except (Exception, ) as error:
            logger.error(f'Ошибка сервера: {error}')
            return JsonResponse({'error': f'Ошибка сервера: {error}'}, status=500)
    return wrapped

# Декоратор для проверки наличия токена
def check_session(func):
    def wrapped(*args, **kwargs):
        try:
            token = [*args][0].COOKIES.get('token')
            if not token:
                raise ObjectDoesNotExist
            session = UserSession.objects.get(session_token=token)
            kwargs['data'] = { 'session': session }
            response = func(*args, **kwargs)
            return response
        except ObjectDoesNotExist:
            logger.error('Запрос ресурсов сервера без авторизации')
            return JsonResponse({'error': 'Вы не авторизованы'}, status=401)
        except (Exception, ) as error:
            logger.error(f'Ошибка сервера: {error}')
            return JsonResponse({'error': f'Ошибка сервера: {error}'}, status=500)
    return wrapped

# Декоратор для проверки статуса администратора
def check_status_admin(func):
    def wrapped(*args, **kwargs):
        user = kwargs['data']['session'].user_id
        try:
            if user.status_admin == True:
                response = func(*args, **kwargs)
                return response
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            logger.error(f'Пользователь с id: {user.id} запрашивает недоступный ресурс')
            return JsonResponse({'error': 'Нет доступа к указанному ресурсу'}, status=403)
    return wrapped
