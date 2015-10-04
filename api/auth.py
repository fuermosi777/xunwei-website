from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import *
import tools
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.core.files.base import ContentFile
import urllib2
import uuid
import mimetypes
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
from datetime import datetime
import calendar
import jwt_helper
import re

@csrf_exempt
def check_user_exist(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    email = request.POST.get('email', None)
    user_exists = False
    if not email:
        return HttpResponse(status=404)
    try:
        user = User.objects.get(username=email)
        user_exists = True
    except:
        user_exists = False
    res = {
        'status': user_exists
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def check_status(request):
    status = False
    msg = ''
    e = ''
    u = ''
    if request.method != 'POST':
        return HttpResponse(status=403)
    token = request.POST.get('token', None)
    if not token:
        return HttpResponse(status=404)
    try:
        data = jwt_helper.decode(token)
    except:
        data = None
        msg = 'Error'

    if data:
        now = calendar.timegm(datetime.utcnow().utctimetuple())
        
        if now > data['expire']:
            msg = 'User expired'
        else:
            try:
                user = User.objects.get(username=data['email'])
                e = user.username
                u = user.first_name
                status = True
            except:
                msg = 'User does not exist'

    res = {
        'status': status,
        'msg': msg,
        'email': e,
        'username': u
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def login(request):
    """
    token content:
        - email (username)
        - username (display name | firstname in Django)
        - password
        - remember
        - expire
    """
    status = False
    msg = ''
    token = ''
    e = ''
    name = ''

    if request.method != 'POST':
        return HttpResponse(status=403)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    expire = calendar.timegm(datetime.utcnow().utctimetuple()) + 2629743
    if None in (email, password):
        return HttpResponse(status=404)

    # get the user
    try:
        user = User.objects.get(username=email)
        e = user.username
        name = user.first_name
    except:
        user = None
        msg = 'User not exists'

    # check pswd
    if user:
        if user.check_password(password):
            status = True
            stuff = {
                'email': email,
                'expire': expire,
            }
            token = jwt_helper.encode(stuff)
        else:
            msg = 'Incorrect password'

    res = {
        'status': status,
        'msg': msg,
        'token': token,
        'email': e,
        'username': name,
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def signup(request):
    """
    token content:
        - email (username)
        - username (display name | firstname in Django)
        - password
        - remember
        - expire
    """
    status = False
    msg = ''
    token = ''

    if request.method != 'POST':
        return HttpResponse(status=403)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    username = request.POST.get('username', None)
    expire = calendar.timegm(datetime.utcnow().utctimetuple()) + 2629743
    if None in (email, password, username):
        return HttpResponse(status=404)
    
    # validate
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        msg = 'Email not valid'
    elif len(username) < 2:
        msg = 'Username too short'
    elif len(password) < 4:
        msg = 'Password too short'
    else:
        # get the user
        try:
            user = User.objects.create_user(
                username=email,
                password=password,
                first_name=username
            )
            status = True
        except:
            user = None
            msg = 'User already exists'

        # check pswd
        if user:
            stuff = {
                'email': email,
                'expire': expire,
            }
            token = jwt_helper.encode(stuff)

    res = {
        'status': status,
        'msg': msg,
        'token': token,
        'email': email,
        'username': username,
    }
    return JsonResponse(res, safe=False)