# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from wechat.models import *
from datetime import datetime

@csrf_exempt
def wechat(request):
    content = ''

    root = ET.fromstring(request.body)    
    msg_type = root.find('MsgType').text
    from_user = root.find('FromUserName').text
    if msg_type == 'text':
        msg = root.find('Content').text.encode('utf-8')

        # get or create a new user
        try:
            user = Wechat_user.get(wechat_user=from_user)
        except:
            user = Wechat_user(wechat_user=from_user)
            user.save()

        # create a new session or get an existing one
        try:
            session = Session.objects.filter(wechat_user=user).latest()
            diff = datetime.now() - session.datetime
            if diff.minutes > 10:
                session = None
                session = Session(wechat_user=user)
        except:
            session = Session(wechat_user=user)
        # save session or refresh session 
        session.save()

        if not user.hot_area:
            content = '想看到最新鲜，最真实，最准确的美食信息么，您现在在哪里？（目前寻味支持“纽约”和“湾区”）'
        else:
            content = '知道你的位置了，然后呢？'

    # not support yet
    else:
        content = '很抱歉，寻味目前还不支持这种格式。'
    
    context = {
        'to': from_user,
        'content': content,
    }
    return render(request, 'text.xml', context, content_type="application/xhtml+xml")