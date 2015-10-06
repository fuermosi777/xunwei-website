from django.shortcuts import render
from django.http import HttpResponse
import hashlib

TOKEN = 'BTSvezvfX1'

# Create your views here.
def wechat(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    token = TOKEN

    temp_list = [token, timestamp, nonce]
    sorted_list = sorted(temp_list)
    temp_list = ''.join(sorted_list)
    temp_list = hashlib.sha1(temp_list)

    if temp_list.hexdigest() == signature:
        return HttpResponse(echostr)
    else:
        return False