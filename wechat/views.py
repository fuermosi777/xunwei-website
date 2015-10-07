from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def wechat(request):
    res = request.body
    return HttpResponse('success')