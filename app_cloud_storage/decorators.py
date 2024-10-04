# from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Декоратор для входа в систему
def app_enter(func):
    def wrapped(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'does not exist'}, status=404)
        except (Exception, ) as error:
            return JsonResponse({'error': f'{error}'}, status=500)
    return wrapped