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
from django.views.decorators.csrf import csrf_exempt
import pytz
from django.utils.translation import ugettext, ungettext
from django.core.validators import validate_email
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives

# userful tools
# for phone number format
def _phone_format(phone):
	num_3 = '(' + phone[:3] + ')'
	num_3_6 = ' ' + phone[3:6] + '-'
	num_6_10 = phone[6:10]
	result = num_3 + num_3_6 + num_6_10
	return result

def _if_null_then_blank(value):
	if not value:
		return ""

def _website_format(website):
    if website:
        return website
    else:
        return '暂无信息'

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
        avg_price = '暂无价格'
    return avg_price

def _formatStar(star):
    if not star:
        star = u'暂无评分'
    else:
        star = math.floor(10*star)/10*2
    star = unicode(star)
    return star

def _nDaysAgo(date):
    delta = datetime.datetime.now(pytz.utc) - date

    num_years = delta.days / 365
    if (num_years > 0):
        return ungettext(u"%d 年前", u"%d 年前", num_years) % num_years

    num_weeks = delta.days / 7
    if (num_weeks > 0):
        return ungettext(u"%d 周前", u"%d 周前", num_weeks) % num_weeks

    if (delta.days > 0):
        return ungettext(u"%d 天前", u"%d 天前", delta.days) % delta.days

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return ungettext(u"%d 小时前", u"%d 小时前", num_hours) % num_hours

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return ungettext(u"%d 分钟前", u"%d 分钟前", num_minutes) % num_minutes

    return ugettext(u"刚刚")

# =========================================================================================   
# iOS API
def restaurants(request):
	amount = request.GET.get('amount', None)
	keyword = request.GET.get('keyword', None)
	lng = request.GET.get('lng', None)
	lat = request.GET.get('lat', None)
	restaurant_id = request.GET.get('restaurant_id', None)
	span = request.GET.get('span', None)
	city = request.GET.get('city', None)

	restaurant = Restaurant.objects.all().order_by('?').annotate(star=Avg('review__star'),price=Avg('review__price'))

	if keyword:
		lst = [
			Q(name__icontains=keyword),
			Q(name2__icontains=keyword),
			Q(subcategory__name__icontains=keyword),
		]
		restaurant = restaurant.filter(reduce(OR,lst))

	if lat and lng:
		spanS = float(span) / 3.7
		lat_up = float(lat) + spanS
		lat_bo = float(lat) - spanS
		lng_up = float(lng) + spanS
		lng_bo = float(lng) - spanS
		restaurant = restaurant.filter(latitude__gte=lat_bo,latitude__lte=lat_up,longitude__gte=lng_bo,longitude__lte=lng_up)

	if city:
		lst2 = [
			Q(city__city__icontains=city),
			Q(city__region__icontains=city),
			Q(postcode__postcode__icontains=city),
		]
		restaurant = restaurant.filter(reduce(OR,lst2))

	restaurant = restaurant.order_by("priority")

	if amount:
		restaurant = restaurant[:amount]

	if restaurant_id:
		restaurant = restaurant.filter(id=restaurant_id)

	for r in restaurant:
		r.review = Review.objects.filter(restaurant=r).order_by('-review_date')[:40]
		try:
			r.review_photo = Review_photo.objects.filter(review__restaurant=r)
		except:
			r.review_photo = None

	data = [{
            'id':r.id,
            'name':r.name,
            'name2': r.name2, 
            'star': _formatStar(r.star), 
            'price':_avg_price(r.price),
            'description': r.description,
            'photo': 'http://xun-wei.com%s'%r.photo.url,
            'website': _website_format(r.website), 
            'phone': _phone_format(r.phone),
            'street1': r.street1,
            'street2': '',
            'city': r.city.city,
            'latitude': unicode(r.latitude),
            'longitude': unicode(r.longitude),
            'postcode': r.postcode.postcode,
            'subcategory':[r2.name for r2 in r.subcategory.all()],
            'review':[{
                'review':r2.review,
                'user':r2.user.userprofile.nickname,
                'username':r2.user.username,
                'avatar':'http://xun-wei.com%s'%r2.user.userprofile.avatar.url,
                'date':_nDaysAgo(r2.review_date),
                'star':_formatStar(r2.star),
                'price':_avg_price(r2.price),
			} for r2 in r.review],
			'review_photo':[{
				'photo':'http://xun-wei.com%s'%r3.photo.url,
				'user':r3.review.user.userprofile.nickname,
			} for r3 in r.review_photo]
	} for r in restaurant]

	for d in data:
		if not d['review']:
			d['review'] = [{
				'review':'暂无评论',
			}]

	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@csrf_exempt
def signin(request):
	status = 0 # -1 weird error
	msg = None
	userinfo = None

	if request.method != 'POST':
		raise Http404
	else:
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)

		# check if user exists
		try:
			user = User.objects.get(username=username)
		except:
			user = None

		# if user exists then check if user has correct pswd
		if user:
			check = user.check_password(password)

			if check:
				status = 1
				userinfo = {
					'id': user.id,
					'username': user.username,
					'avatar': 'http://xun-wei.com%s'%user.userprofile.avatar.url,
				}
						
			else:
				msg = "用户名和密码不匹配"
		else:
			msg = "用户不存在"

		data = {
			'status': status,
			'msg': msg,
			'userinfo': userinfo,
		}

	return HttpResponse(simplejson.dumps(data), content_type='application/json')

@csrf_exempt
def signup(request):
	if request.method != 'POST':
		raise Http404
	else:
		status = 0
		msg = None
		userinfo = None

		username = request.POST.get('username', None)
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)

		# validate variables
		if not username or not email or not password:
			msg = '错误信息'

		if len(username) < 6 or len(username) > 30:
			msg = '用户名长度应该在6-30之间'

		if len(password) < 6 or len(password) > 30:
			msg = '密码长度应该在6-30之间'

		try:
			validate_email(email)
		except:
			msg = 'Email地址不正确'

		try:
			user = User.objects.get(username=username)
			msg = '用户名已经存在'
		except:
			pass
		try:
			email = User.objects.get(email=email)
			msg = 'Email地址已经存在'
		except:
			pass	

		if not msg:
			# create a new user (inactive)
			user = User.objects.create_user(username,email,password)
			user.save()

			up = UserProfile(user_id=user.id,nickname=username) # add a default avatar
			up.save()

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
				msg = "发送失败"

			if not msg:
				status = 1 # success
				userinfo = {
					'id': user.id,
					'username': user.username,
					'avatar': 'http://xun-wei.com%s'%user.userprofile.avatar.url,
				}
		else:
			pass
		data = {
			'status':status,
			'msg':msg,
			'userinfo':userinfo,
		}
		return HttpResponse(simplejson.dumps(data), content_type='application/json')

@csrf_exempt
def review(request):
	if request.method != 'POST':
		raise Http404
	else:
		status = 0
		msg = None

		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		review = request.POST.get('review', None)
		star = request.POST.get('star', None)
		price = request.POST.get('price', None)
		restaurant_id = request.POST.get('restaurantID', None)
		photos = request.FILES.getlist("photo")

		if (not username or not password or not review or not star or not price or not restaurant_id):
			msg = "信息填写不全"
		try:
			restaurant = Restaurant.objects.get(id=restaurant_id)
		except:
			msg = "找不到餐馆"
		try:
			user = User.objects.get(username=username)
		except:
			user = None
			msg = "找不到用户"

		try:
			star = int(star)
			price = int(price)
		except:
			msg = "价格评分格式不正确"

		if star < 1 or star > 5 or price < 1 or price > 5:
			msg = "价格或评分不正确"

		if user:
			check = user.check_password(password)
			if not check:
				msg = "用户无法通过验证"
		if not msg:
			review = Review(review=review,star=star,price=price,user=user,restaurant=restaurant)
			try:
				review.save()
				status = 1
			except:
				msg = "未知错误"
			if photos:
				for p in photos:
					rp = Review_photo(photo=p, review=review)
					rp.save()

		data = {
			'status':status,
			'msg':msg,
		}
		return HttpResponse(simplejson.dumps(data), content_type='application/json')

@csrf_exempt
def user(request):
	if request.method != 'POST':
		raise Http404
	else:
		status = 0
		msg = None
		info = None

		username = request.POST.get('username', None)

		if not username:
			msg = "信息填写不全"
		try:
			user = User.objects.get(username=username)
		except:
			user = None
			msg = "找不到用户"

		if not msg:
			review = Review.objects.filter(user=user).order_by('-review_date')[:30]
			status = Status.objects.filter(user=user, status=2).order_by('-id') # 2 - want to eat

			info = {
				'username': user.username,
				'avatar': 'http://xun-wei.com%s'%user.userprofile.avatar.url,
				'review_num': review.count(),
				'liked_num': status.count(),
				'date_joined': _nDaysAgo(user.date_joined),
				'reviews': [{
					'review': r.review,
					'review_date': _nDaysAgo(r.review_date),
					'star': _formatStar(r.star),
					'restaurant_name': r.restaurant.name,
					'restaurant_photo': 'http://xun-wei.com%s'%r.restaurant.photo.url,
				} for r in review],
				'liked': [{
					'id': s.restaurant_id,
					'name': s.restaurant.name,
					'photo': 'http://xun-wei.com%s'%s.restaurant.photo.url,
					'street1': s.restaurant.street1,
		            'street2': s.restaurant.street2,
		            'city': s.restaurant.city.city,
		            'postcode': s.restaurant.postcode.postcode,
		            'subcategory':[r.name for r in s.restaurant.subcategory.all()],
				} for s in status],
			} 

			status = 1

		data = {
			'status':status,
			'msg':msg,
			'info':info,
		}
		return HttpResponse(simplejson.dumps(data), content_type='application/json')

@csrf_exempt
def userprofile(request):
	status = 0
	msg = None
	info = None

	image = request.FILES.get("avatar", None)
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)

	if not username or not password:
		msg = "信息填写不全"

	try:
		user = User.objects.get(username=username)
	except:
		user = None
		msg = "找不到用户"

	if user:
		check = user.check_password(password)
		if not check:
			msg = "用户无法通过验证"

	if not msg:
		up = UserProfile.objects.get(user=user)
		up.avatar = image
		up.save()

		if image:
			status = 1

	data = {
		'status':status,
		'msg':msg,
		'info':{
			'avatar': 'http://xun-wei.com%s'%user.userprofile.avatar.url,
		}
	}
	return HttpResponse(simplejson.dumps(data), content_type='application/json')

def ad(request):
	ad = Ad.objects.all()
	data = [{
			"photo": 'http://xun-wei.com%s'%a.photo.url,
			"link": a.link
		} for a in ad]
	return HttpResponse(simplejson.dumps(data), content_type='application/json')

@csrf_exempt
def status(request): # 1 eaten 2 want to eat
	status = 0
	msg = None
	is_liked = 0

	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		restaurant_id = request.POST.get('restaurant_id', None)
		action = request.POST.get('action', None)

		if not username or not restaurant_id or not action:
			raise Http404

		user = get_object_or_404(User,username=username)
		restaurant = get_object_or_404(Restaurant,id=restaurant_id)

		if user:
			check = user.check_password(password)

		if not check:
			msg = '用户名密码错误'

		try:
			s = Status.objects.get(user=user,restaurant=restaurant)
		except:
			s = None

		if not msg:
			if action == 'GET':
				if s:
					is_liked = 1
					
				else:
					is_liked = 0
				status = 1

			if action == 'POST':
				if s:
					s.delete()
					is_liked = 0
				else:
					s = Status(status=2, user=user, restaurant=restaurant)
					s.save()
					is_liked = 1
				status = 1

	else:
		raise Http404

	data = {
		'status': status,
		'msg': msg,
		'is_liked': is_liked,
	}
	return HttpResponse(simplejson.dumps(data), content_type='application/json')

def webpage_restaurant(request, offset):
	try: # there is a restaurant
		offset = int(offset)
	except ValueError:
		raise Http404

	return HttpResponseRedirect("/restaurant/%s"%offset)