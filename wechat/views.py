# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET

@csrf_exempt
def wechat(request):
    content = ''

    root = ET.fromstring(request.body)    
    msg_type = root.find('MsgType').text
    from_user = root.find('FromUserName').text
    if msg_type == 'text':
        msg = root.find('Content').text.encode('utf-8')
        content = '你好'
        if '漂亮' in msg:
            content = '我家宝宝'
    else:
        content = '很抱歉，寻味目前还不支持这种格式。'
    
    context = {
        'to': from_user,
        'content': content,
    }
    return render(request, 'text.xml', context, content_type="application/xhtml+xml")