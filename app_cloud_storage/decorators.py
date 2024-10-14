from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from app_cloud_storage.models import UserSession

# Декоратор для входа в систему
def app_enter(func):
    def wrapped(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        # except ObjectDoesNotExist:
        #     return JsonResponse({'error': 'does not exist'}, status=404)
        except (Exception, ) as error:
            return JsonResponse({'error': f'Ошибка сервера: {error}'}, status=500)
    return wrapped

# Декоратор для проверки наличия токена
def check_session(func):
    def wrapped(*args, **kwargs):
        try:
            session = UserSession.objects.get(session_token=[*args][0].headers['Authorization'])
            kwargs['data'] = { 'session': session }
            response = func(*args, **kwargs)
            return response
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Вы не авторизованы'}, status=404)
        except (Exception, ) as error:
            return JsonResponse({'error': f'Ошибка сервера: {error}'}, status=500)
    return wrapped
