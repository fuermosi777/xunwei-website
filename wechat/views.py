# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def wechat(request):
    res = request.body
    context = {
        'content': u'你好'
    }
    return render(request, 'text.xml', context, content_type="application/xhtml+xml")