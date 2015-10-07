# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from wechat.models import *
from datetime import datetime
from django.db.models import Q

@csrf_exempt
def wechat(request):
    content = ''
    post = None
    template = 'text.xml'

    root = ET.fromstring(request.body)    
    msg_type = root.find('MsgType').text
    from_user = root.find('FromUserName').text
    if msg_type == 'text':
        msg = root.find('Content').text.encode('utf-8')

        # get or create a new user
        try:
            user = Wechat_user.objects.get(wechat_user=from_user)
        except:
            user = Wechat_user(wechat_user=from_user)
            user.save()

        # create a new session or get an existing one
        try:
            session = Wechat_session.objects.filter(wechat_user=user).latest()
            diff = datetime.now() - session.datetime
            if diff.minutes > 10:
                # start a new session
                session = Wechat_session(wechat_user=user)
        except:
            session = Wechat_session(wechat_user=user)
        # save session or refresh session 
        session.save()

        if not user.hot_area:
            content = '想看到最新鲜，最真实，最准确的美食信息么，您现在在哪里？（目前寻味支持“纽约”和“湾区”）'
            if msg == '纽约' or msg == '湾区':
                user.hot_area = Hot_area.objects.get(name=msg)
                user.save()
                content = '您想吃点什么？（中餐/火锅/烧烤/日料/川菜...）'
        else:
            post = Post.objects.filter(is_approved=True, hot_area=user.hot_area).filter(Q(title__icontains=msg) | Q(business__tag__name__icontains=msg) | Q(business__name__icontains=msg) | Q(business__name2__icontains=msg)).order_by('?')[:5]
            if post:
                template = 'news.xml'
            else:
                content = '很抱歉，找不到任何关于“%s”的内容'%msg


    # not support yet
    else:
        content = '很抱歉，寻味目前还不支持这种格式。'
    
    context = {
        'to': from_user,
        'content': content,
        'post': post,
    }
    return render(request, template, context, content_type="application/xhtml+xml")