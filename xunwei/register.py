#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from views import restaurant
from app.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import random
from django.db.models import Q
from django.core.validators import validate_email
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# save image from url
def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.avatar.save("image.jpg", File(img_temp), save=True)

def register(request):
    error = None
    if request.user.is_authenticated(): #if user is logged in
        return HttpResponseRedirect("/accounts/profile/%s"%request.user.id)

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        if not username or not password or not email:
            error = "信息填写不全"
        if len(username) < 6 or len(username) > 30:
            error = '用户名长度应该在6-30之间'
        if len(password) < 6 or len(password) > 30:
            error = '密码长度应该在6-30之间'
        try:
            validate_email(email)
        except:
            error = 'Email地址不正确'
        try:
            user = User.objects.get(username=username)
            error = '用户名已经存在'
        except:
            pass
        try:
            email = User.objects.get(email=email)
            error = 'Email地址已经存在'
        except:
            pass
        if not error:
            # create a new user (inactive)
            user = User.objects.create_user(username,email,password)
            user.save()
            up = UserProfile(user_id=user.id,nickname=username) # add a default avatar
            up.save()

            user_new = authenticate(username=username, password=password)
            login(request, user_new)
            # send a welcome Email
            plaintext = get_template('email/email.txt')
            htmly = get_template('email/email.html')
            d = Context({ 
                'username': username,
                'email': email,
                'title': 'Welcome',
                'content': '欢迎加入寻味纽约'
            })
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            email_msg = EmailMultiAlternatives('欢迎加入寻味', text_content, 'customer@xun-wei.com', [email])
            email_msg.attach_alternative(html_content, "text/html")
            try:
                email_msg.send()
            except:
                error = "发送失败"

            return HttpResponseRedirect('/accounts/register/upload/')
        else:
            pass
    context = {
        'error':error,
    }
    return render(request,"registration/register.html", context)

@login_required
def register_upload(request):
    error = None
    success = None
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST': # user wants to change basic information
        avatar = request.FILES.get("avatar", None)
        nickname = request.POST.get("nickname", None)
        introduction = request.POST.get("introduction", None)
        if not avatar or not nickname:
            error = "信息填写不全"   

        if not error:
            userprofile.avatar = avatar
            userprofile.introduction = introduction
            userprofile.save()
            return HttpResponseRedirect("/accounts/profile/%s/"%request.user.id)
        else:
            pass
    context = {
        'error':error,
    }
    return render(request,"registration/register_upload.html", context)

def forget_password(request):
    error = None
    email_sent = False
    template = "registration/forget_password.html"
    try:
        not request.user.is_authenticated
    except:
        return HttpResponseRedirect('/accounts/profile/%s'%request.user.id)
    if request.method == 'POST':
        try:
            username = request.POST['username']
        except:
            error = "请填写用户名"
        try:
            email = request.POST['email']
        except:
            error = "请填写Email"
        try:
            user = User.objects.get(username=username)
        except:
            error = "不存在该用户"
        if user.email != email:
            error = "用户名和Email不匹配"
        elif error == None:
            confirmation_code = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(33)])
            up = UserProfile.objects.get(user=user)
            up.confirmation_code = confirmation_code
            up.save() # save to userprofile

            # get template
            # and send forget pswd Email
            plaintext = get_template('email/forget_password_email.txt')
            htmly     = get_template('email/forget_password_email.html')

            d = Context({ 
                'username': username,
                'email': request.POST['email'],
                'confirmation_code':confirmation_code,
             })

            subject, from_email, to = '寻味|重设密码', 'customer@xun-wei.com', request.POST['email']
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                error = '错误的Email地址'
            # mark email sent status as true
            email_sent = True

        context = {
            'error':error,
            'email_sent':email_sent,
        }
        return render(request,template,context)
    context = {
        'error':error,
        'email_sent':email_sent,
    }
    return render(request,template,context)

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/%s/"%request.user.id)

    error = None
    redirect_to = request.GET.get("next", None)
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect("/accounts/profile/%s/"%user.id)
        else:
            error = "用户名和密码不匹配"

    context = {
        "error": error,
    }
    return render(request,"registration/login.html", context)


def reset_password(request):
    try:
        not request.user.is_authenticated
    except:
        return HttpResponseRedirect('/accounts/profile/%s'%request.user.id)
    try:
        key = request.GET['key']
        key = unicode(key)
    except:
        raise Http404
    error = None
    try:
        userprofile = UserProfile.objects.exclude(confirmation_code__exact='').get(confirmation_code=key)
    except:
        raise Http404
    if request.method == 'POST':
        form = SetPasswordForm(user=userprofile.user, data=request.POST)
        if form.is_valid():
            form.save()
            userprofile.confirmation_code = ''
            userprofile.save()
            return HttpResponseRedirect('/accounts/profile/%s/'%userprofile.user.id)
        else: # if user change password is not correct
            error = "密码输入错误"
    template = "registration/reset_password.html"
    passwordresetform = SetPasswordForm(user=userprofile.user,data=request.POST)
    context = {
        'error':error,
        'passwordresetform':passwordresetform,
    }
    return render(request,template,context)

def login_error(request):
    raise Http404