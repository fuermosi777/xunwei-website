#!/usr/bin/python
# -*- coding: utf-8 -*-
#from django.http import HttpResponse
#from django.template.loader import get_template
#from django.template import Context

from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
import datetime
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from app.models import *
from django.db.models import Q
from django.utils import simplejson
from django.http import Http404
from forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.template import Context
from operator import __or__ as OR
import math
from bs4 import BeautifulSoup
import random
from django.core import serializers
# userful tools
# for phone number format
def _phone_format(phone):
    num_3 = '(' + phone[:3] + ')'
    num_3_6 = ' ' + phone[3:6] + '-'
    num_6_10 = phone[6:10]
    result = num_3 + num_3_6 + num_6_10
    return result

def _avg_price(average_price):
    if average_price >= 1 and average_price < 2:
        avg_price = '低于$10'
    elif average_price >=2 and average_price < 3:
        avg_price = '$10-30'
    elif average_price >=3 and average_price < 4:
        avg_price = '$30-50'
    elif average_price >=4 and average_price < 5:
        avg_price = '$50-80'
    elif average_price >=5:
        avg_price = '$80+'
    else:
        avg_price = '暂无'
    return avg_price

def _formatStar(star):
    if not star:
        star = '0.0'
    else:
        star = math.floor(10*star)/10*2
    star = unicode(star)
    return star

def home_new(request):
    return render(request,"home_new.html")

# begin views def
def homepage(request):
    citys = City.objects.filter().annotate(restaurant_num=Count("restaurant")).order_by('-restaurant_num')[:10]
    for c in citys:
        c.restaurant = Restaurant.objects.filter(city=c).order_by('?')[:8]

    context = {
        'citys':citys,
    }
    return render(request, "homepage.html",context)

@login_required
def after_login(request):
    return HttpResponseRedirect('/accounts/profile/%d/'%request.user.id)

def profile(request,offset):
    try:
        offset = int(offset)
    except:
        raise Http404
    try:
        user = User.objects.get(id=offset)
    except:
        raise Http404
    review = Review.objects.filter(user=user).order_by('-review_date','restaurant__name')
    status = Status.objects.filter(user=user,status=2).order_by('-status_date')

    context = {
        'user':user,
        'review':review,
        'status':status,
    }
    return render(request, 'profile.html', context)

def restaurant(request,offset):
    errors = []
    try: # there is a restaurant
        offset = int(offset)
    except ValueError:
        raise Http404
    try: # page is valid -> find the restaurant
        restaurant = Restaurant.objects.get(id=offset)
    except Restaurant.DoesNotExist:
        raise Http404
    # similar restaurant
    subcategory = restaurant.subcategory.all().order_by('?')[0]
    similar_restaurant = Restaurant.objects.filter(subcategory=subcategory).order_by('?')[:4]
    # nearby restaurant
    nearby_restaurant = Restaurant.objects.filter(city=restaurant.city).order_by('?')[:4]
    # review
    review = Review.objects.filter(restaurant=restaurant).order_by('-review_date')
    restaurant.star = _formatStar(review.aggregate(Avg('star'))['star__avg'])
    restaurant.price = _avg_price(review.aggregate(Avg('price'))['price__avg'])

    review = review[:30]

    restaurant.phone = _phone_format(restaurant.phone)

    context = {
        "restaurant": restaurant,
        "similar_restaurant": similar_restaurant,
        "nearby_restaurant": nearby_restaurant,
        "review":review,
    }
    return render(request, "restaurant.html",context) # with status

def search(request):
    error = None

    keyword = request.GET.get('keyword', None)
    lng = request.GET.get('lng', None)
    lat = request.GET.get('lat', None)
    span = request.GET.get('span', None)
    city = request.GET.get('city', None)
    if not city:
        city = "New York"

    restaurant = Restaurant.objects.all().order_by('?').annotate(star=Avg('review__star'),price=Avg('review__price'))

    if keyword:
        keyword_lst = [
            Q(name__icontains=keyword),
            Q(name2__icontains=keyword),
            Q(city__state__state__icontains=keyword),
            Q(city__city__icontains=keyword),
            Q(city__region__icontains=keyword),
            Q(postcode__postcode__icontains=keyword),
            Q(subcategory__name__icontains=keyword),
        ]
        restaurant = restaurant.filter(reduce(OR,keyword_lst))

    if lat and lng:
        spanS = float(span) / 3.7
        lat_up = float(lat) + spanS
        lat_bo = float(lat) - spanS
        lng_up = float(lng) + spanS
        lng_bo = float(lng) - spanS
        restaurant = restaurant.filter(latitude__gte=lat_bo,latitude__lte=lat_up,longitude__gte=lng_bo,longitude__lte=lng_up)

    if city:
        city_lst = [
            Q(city__city__icontains=city),
            Q(city__region__icontains=city),
        ]
        restaurant = restaurant.filter(reduce(OR,city_lst))

    # check the result    
    if restaurant:
        initial_latitude = restaurant[0].latitude
        initial_longitude = restaurant[0].longitude
        order = 0
        for r in restaurant:
            r.order = order + 1
            order += 1
            try:
                r.average_star = math.floor(10*r.average_star)/10*2
            except:
                r.average_star = '暂无评分'
            # format phone
            if r.phone:
                r.phone = _phone_format(r.phone)
            else:
                pass
            # get review
            try:
                r.review = Review.objects.filter(restaurant=r).order_by('?')[:1][0]
            except:
                r.review = None
    else:
        error = '很抱歉，没有找到相关的餐馆'
        initial_latitude = 40.73082
        initial_longitude = -73.9974
        restaurant = None

    context = {
        'error':error,
        'restaurant':restaurant,
        'initial_longitude':initial_longitude,
        'initial_latitude':initial_latitude,
        'keyword':keyword,
    }
    return render(request,'search.html',context)

def test(request):
    lst = []
    restaurant = Restaurant.objects.all()

    return render(request,'test.html',context)

#----------------------static pages---------------------------
def disclaimer(request):
    return render(request,'static/disclaimer.html')
def about_us(request):
    return render(request,'static/about_us.html')