from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def registrationUser(request):
    body_unicode = request.body.decode('utf-8')
    json_body = json.loads(body_unicode)
    del json_body['password']
    print('запрос1', json_body)
    return JsonResponse(json_body, status=201)