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
import jwt_helper
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def business_list(request):
    start = request.GET.get('start', None) # require
    hot_area = request.GET.get('hot_area', None) # optional
    tag = request.GET.get('tag', None) # optional

    business = Business.objects.all()

    if hot_area:
        business = business.filter(hot_area__name=hot_area)
    if tag:
        business = business.filter(tag__name=tag)

    start = int(start)
    business = business[start:start+30]
    res = [tools.get_business_json(b) for b in business]
    return JsonResponse(res, safe=False)


def post_list(request):
    start = request.GET.get('start', None) # required
    business_id = request.GET.get('business_id', None) # optional
    hot_area = request.GET.get('hot_area', None) # optional
    tag = request.GET.get('tag', None) # optional
    q = request.GET.get('q', None) # optional

    post = Post.objects.filter(is_approved=True).order_by('-id')
    if business_id:
        business = Business.objects.get(id=business_id)
        post = post.filter(business=business)
    if hot_area:
        post = post.filter(business__hot_area__name=hot_area)
    if tag:
        post = post.filter(business__tag__name=tag)
    if q:
        post = post.filter(Q(business__tag__name__icontains=q) | Q(business__name__icontains=q) | Q(business__name2__icontains=q))

    start = int(start)
    post = post[start:start+30]
    res = [{
        'id': p.id,
        'title': p.title,
        'preview': p.preview,
        'body': p.body,
        'source': p.source,
        'business': tools.get_business_json(p.business)
    } for p in post]
    return JsonResponse(res, safe=False)

def post(request):
    post_id = request.GET.get('post_id', None)

    post = Post.objects.get(id=post_id)
    if not post:
        return HttpResponse(status=404)
    res = {
        'id': post.id,
        'title': post.title,
        'preview': post.preview,
        'body': post.body,
        'source': post.source,
        'business': tools.get_business_json(post.business)
    }
    return JsonResponse(res, safe=False)

def business(request):
    business_id = request.GET.get('business_id', None)

    business = Business.objects.get(id=business_id)
    if not business:
        return HttpResponse(status=404)
    res = tools.get_business_json(business)
    return JsonResponse(res, safe=False)    

def tag_list(request):
    tag = Tag.objects.all()
    res = [{
        'name': t.name,
    } for t in tag]
    return JsonResponse(res, safe=False)

@csrf_exempt
def upload_image(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    image = request.POST.get('image', None)
    if ',' in image:
        _, image = image.split(',')
    image_data = b64decode(image)
    post_photo = Post_photo()
    post_photo.photo = ContentFile(image_data, 'temp.jpg')
    post_photo.save()
    res = {
        'link': post_photo.photo.url,
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def upload_image_url(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    image_url = request.POST.get('image_url', None)
    source_domain = request.POST.get('source_domain', None)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding': 'none',
        # 'Accept-Language': 'en-US,en;q=0.8',
        # 'Connection': 'keep-alive',
        'referer': source_domain,
    }

    ext = mimetypes.guess_extension(mimetypes.guess_type(image_url)[0])
    req = urllib2.Request(image_url, headers=headers)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib2.urlopen(req).read())
    img_temp.flush()

    post_photo = Post_photo()
    post_photo.photo.save('%s%s'%(uuid.uuid4(), ext), File(img_temp))
    post_photo.save()

    res = {
        'link': post_photo.photo.url,
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def add_post(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    token = request.POST.get('token', None)    
    title = request.POST.get('title', None)
    preview = request.POST.get('preview', None)
    body = request.POST.get('body', None)

    decode = jwt_helper.decode(token)
    try:
        user = User.objects.get(username=decode['email'])
    except:
        user = None
        return HttpResponse(status=403)

    if None in (token, title, body, preview):
        return HttpResponse(status=500)

    post = Post(
        title=title,
        preview=preview,
        body=body,
        business_id=20,
        user=user
    )
    post.save()
    try:
        post.save()
    except:
        pass

    res = {
        'msg': 'success',
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def secret_add_post(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    token = request.POST.get('token', None)    
    business_id = request.POST.get('business_id', None)
    source = request.POST.get('source', None)
    title = request.POST.get('title', None)
    preview = request.POST.get('preview', None)
    body = request.POST.get('body', None)

    if None in (token, business_id, source, title, preview, body):
        return HttpResponse(status=500)
    if token != 'xw1':
        return HttpResponse(status=403)

    business = Business.objects.get(id=business_id)

    post = Post(
        title=title,
        preview=preview,
        body=body,
        source=source,
        business=business,
        is_approved=True,
    )
    post.save()
    try:
        post.save()
    except:
        pass

    res = {
        'msg': 'success',
    }
    return JsonResponse(res, safe=False)

@csrf_exempt
def star_post(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    post_id = request.POST.get('post_id', None)
    token = request.POST.get('token', None)
    decode = jwt_helper.decode(token)
    user = User.objects.get(username=decode['email'])
    try:
        star = Star.objects.get(post_id=post_id, user=user)
        star.delete()
    except:
        star = Star(post_id=post_id, user=user)
        star.save()
    star_num = Star.objects.filter(post_id=post_id).count()
    res = {
        'star_num': star_num
    }
    return JsonResponse(res, safe=False)

def post_star(request):
    post_id = request.GET.get('post_id', None)
    star_num = Star.objects.filter(post_id=post_id).count()
    res = {
        'star_num': star_num
    }
    return JsonResponse(res, safe=False)