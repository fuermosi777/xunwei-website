from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from api.models import *

# Create your views here.
def old(request, restaurant):
    return HttpResponseRedirect('/')

def home(request):
    post = Post.objects.all().order_by('-id')[:100]
    context = {
        'post': post,
    }
    return render(request, 'home.html', context)

def post(request, post_id):
    try:
        post_instance = Post.objects.get(id=post_id)
    except:
        post_instance = None
        return HttpResponseRedirect('/')
    context = {
        'post': post_instance
    }
    return render(request, 'post.html', context)

def business(request, business_id):
    try:
        business_instance = Business.objects.get(id=business_id)
    except:
        business_instance = None
        return HttpResponseRedirect('/')
    post = Post.objects.filter(business=business_instance).order_by('-id')[:50]
    context = {
        'business': business_instance,
        'post': post,
    }
    return render(request, 'business.html', context)

def area(request, area_name):
    try:
        hot_area_instance = Hot_area.objects.get(name=area_name)
    except:
        hot_area_instance = None
        return HttpResponseRedirect('/')
    context = {
        'hot_area': hot_area_instance
    }
    return render(request, 'area.html', context)

def tag(request, tag_name):
    try:
        tag_instance = Tag.objects.get(name=tag_name)
    except:
        tag_instance = None
        return HttpResponseRedirect('/')
    business_instance = Business.objects.filter(tag=tag_instance)
    context = {
        'tag': tag_instance,
        'business': business_instance,
    }
    return render(request, 'tag.html', context)