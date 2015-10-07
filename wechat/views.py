from django.shortcuts import render
from django.http import HttpResponse
import hashlib

# Create your views here.
def wechat(request):
    res = request.body
    return HttpResponse(res)