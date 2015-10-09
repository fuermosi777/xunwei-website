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
    content = None
    template = 'text.xml'
    context = {}

    root = ET.fromstring(request.body)    
    msg_type = root.find('MsgType').text
    from_user = root.find('FromUserName').text

    context['to'] = from_user

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
            session = None
        else:
            session.save()
    except:
        session = None

    if not session:
        session = Wechat_session(wechat_user=user)
        session.save()
        
    if msg_type == 'text':
        # get text message
        msg = root.find('Content').text.encode('utf-8')

        context, template = check_text(user, msg, context, template)

    elif msg_type == 'location':
        lat = float(root.find('Location_X').text)
        lng = float(root.find('Location_Y').text)
        s = 0.01
        try:
            post = Post.objects.filter(is_approved=True, business__latitude__lt=lat+0.01, business__latitude__gt=lat-0.01, business__longitude__lt=lng+0.01, business__longitude__gt=lng-0.01).order_by('?')[:5]
        except:
            post = None
        if post:
            context['post'] = post
            template = 'post.xml'
        else:
            context['content'] = '寻味在您附近没找到靠谱的餐馆...'

    elif msg_type == 'event':
        event = msg_type = root.find('Event').text
        if event == 'subscribe':
            context['content'] = '欢迎关注寻味！您可以发送您所在的地区（纽约或湾区）、邮编、或者直接点击加号发送您的位置给我们。我们会帮你找到最新鲜、丰富的美食信息！您可以直接浏览我们的网站http://xun-wei.com'

    # not support yet
    else:
        context['content'] = '很抱歉，寻味目前还不支持这种格式。'
    
    return render(request, template, context, content_type="application/xhtml+xml")

def check_text(user, msg, context, template):
    # check if feedback
    if msg.startswith('反馈'):
        fb = Feedback(wechat_user=user, content=msg)
        fb.save()
        context['content'] = '您的反馈我们已经收到，谢谢！'
        return (context, template)
    # check if a specific business
    try:
        business = Business.objects.filter(Q(name__iexact=msg) | Q(name2__iexact=msg)).order_by('?')[:5]
    except:
        business = None
    if business:
        context['business'] = business
        template = 'business.xml'
        return (context, template)
    # check hot_area
    try:
        hot_area = Hot_area.objects.get(Q(name__icontains=msg) | Q(other_name__icontains=msg))
    except:
        hot_area = None
    if hot_area:
        user.hot_area = hot_area
        user.save()
        context['content'] = '您想吃点什么？（川菜、火锅、烧烤、米其林...）'
        return (context, template)
    # check postcode
    try:
        msg = int(msg)
    except:
        pass
    if isinstance(msg, int) and len(str(msg)) == 5:
        try:
            post = Post.objects.filter(is_approved=True, business__postcode__number=msg)
        except:
            post = None
        if post:
            context['post'] = post
            template = 'post.xml'
        else:
            context['content'] = '很抱歉，找不到位于邮编%s的餐馆'%msg
        return (context, template)
    # check if user has a location selected
    if not user.hot_area:
        context['content'] = '你想看哪里美食信息？（目前寻味支持纽约和湾区，其他北美地区敬请期待! ^_^）'
        return (context, template)
    # check if tag
    try:
        post = Post.objects.filter(is_approved=True, business__hot_area=user.hot_area).filter(
                    Q(title__icontains=msg) | 
                    Q(business__tag__other_name__icontains=msg) |
                    Q(business__tag__name__icontains=msg) | 
                    Q(business__city__name__icontains=msg) |
                    Q(business__city__other_name__icontains=msg) |
                    Q(business__name__icontains=msg) | 
                    Q(business__name2__icontains=msg)
                ).order_by('?')[:5]
    except:
        post = None
    if post:
        context['post'] = post
        template = 'post.xml'
        return (context, template)
    # fallback
    context['content'] = '很抱歉，找不到任何关于“%s“的内容。请输入地区、菜色或者邮编给寻味，或者直接点击加号发送您的位置给我们。我们会帮你找到最新鲜、丰富的美食信息！'%msg
    return (context, template)