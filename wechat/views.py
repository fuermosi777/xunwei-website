from django.shortcuts import render
from django.http import HttpResponse
import hashlib

def wechat(request):
    res = request.body
    return HttpResponse('success')