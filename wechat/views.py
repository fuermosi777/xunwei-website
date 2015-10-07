# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET

@csrf_exempt
def wechat(request):
    root = ET.fromstring(request.body)
    from_user = root.find('FromUserName').text
    context = {
        'to': from_user,
        'content': '你好'
    }
    return render(request, 'text.xml', context, content_type="application/xhtml+xml")