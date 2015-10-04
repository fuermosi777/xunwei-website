#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models, connection
from django.contrib.auth.models import User
from django import forms
import uuid, os
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db.models import Avg, Count

# add watermark
from xunwei.watermark import ImageWatermark
class Watermark(object):
    def process(self, image):
        watermark = "/home/fuermosi777/webapps/xunwei_static/img/logo_t.png"
        scaled = ImageWatermark(watermark,
            position=('center', 'center'),
            scale=True,
            opacity=1)
        image = scaled.process(image)
        return image

def user_avatar_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext) #use uuid to generate a random name
    return os.path.join('user_avatar', filename)

class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = ProcessedImageField(upload_to=user_avatar_name,default='user_avatar/default/xunwei.jpg',processors=[ResizeToFill(160, 160)],format='JPEG',options={'quality': 80})
    nickname = models.CharField(max_length=100)
    introduction = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=33,blank=True)

class State(models.Model):
    state = models.CharField(max_length=20,unique=True)

    def __unicode__(self):
        return unicode(self.state)

class Postcode(models.Model):
    postcode = models.CharField(max_length=5,unique=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.postcode

class City(models.Model):
    city = models.CharField(max_length=100,unique=True)
    region = models.CharField(max_length=100)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.city

def restaurant_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('restaurant_photo', filename)

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __unicode__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100,unique=True)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name 

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100,blank=True)
    website = models.URLField(blank=True)
    description = models.TextField()
    phone = models.CharField(max_length=12)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City)
    postcode = models.ForeignKey(Postcode)
    latitude = models.DecimalField(max_digits=17, decimal_places=12)
    longitude = models.DecimalField(max_digits=17, decimal_places=12)
    photo = ProcessedImageField(upload_to=restaurant_photo_name,processors=[ResizeToFill(800, 800),Watermark(),],format='JPEG',options={'quality': 80})
    subcategory = models.ManyToManyField(Subcategory)
    priority = models.IntegerField(max_length=2, default=3) # 1 - 顶级推荐 2 - 合作 3 - 一般

    def photo_image(self):
        return '<img style="width:200px;height:200px" src="%s"'%self.photo.url
    photo_image.allow_tags = True

    def display_subcategory(self):
        return ', '.join([s.name for s in self.subcategory.all()])

    def __unicode__(self):
        return self.name

        class Meta:
            ordering = ['name']

class Status(models.Model):
    status = models.IntegerField(max_length=1) # 2
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    status_date = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return unicode(self.status)

class Review(models.Model):
    review = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField()
    price = models.IntegerField()
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)

    def __unicode__(self):
        return self.review

def review_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('review_photo', filename)

class Review_photo(models.Model):
    photo = ProcessedImageField(upload_to=review_photo_name,processors=[ResizeToFill(800, 800),Watermark(),],format='JPEG',options={'quality': 80})
    review = models.ForeignKey(Review)

    def __unicode__(self):
        return self.photo.name

class Journal(models.Model):
    title = models.TextField()
    journal = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    view_num = models.IntegerField(max_length=10,default=0)
    user = models.ForeignKey(User)
    restaurant = models.ManyToManyField(Restaurant,blank=True)

    def __unicode__(self):
        return self.title

# ajax end ---

def attachment_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('attachment_photo', filename)

class Attachment(models.Model):
    photo = ProcessedImageField(upload_to=attachment_photo_name,processors=[ResizeToFill(800, 800),Watermark(),],format='JPEG',options={'quality': 80})
    user = models.ForeignKey(User)

def ad_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('ad_photo', filename)

class Ad(models.Model):
    photo = ProcessedImageField(upload_to=ad_photo_name,format='JPEG')
    link = models.CharField(max_length=100)