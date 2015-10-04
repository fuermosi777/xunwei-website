from django.db import models
import os, uuid
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from froala_editor.fields import FroalaField
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.
class Hot_area(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return unicode(self.name)

class State(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return unicode(self.name)

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Postcode(models.Model):
    number = models.CharField(max_length=5, unique=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.number

def business_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('business_photo', filename)

class Business(models.Model):
    name = models.CharField(max_length=50)
    name2 = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=12)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City)
    postcode = models.ForeignKey(Postcode)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    photo = ProcessedImageField(upload_to=business_photo_name, format='JPEG', options={'quality': 80})
    tag = models.ManyToManyField(Tag)
    hot_area = models.ForeignKey(Hot_area)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    preview = models.TextField(blank=False)
    body = FroalaField(blank=False, options={'plainPaste': True,'defaultImageWidth': 0, 'defaultImageAlignment': 'left', 'pasteImage': True, 'pastedImagesUploadURL': '/api/upload_image/'})
    datetime = models.DateTimeField(auto_now_add=True)
    source = models.URLField(blank=True, max_length=300)
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

def post_photo_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('post_photo', filename)

class Post_photo(models.Model):
    photo = ProcessedImageField(upload_to=post_photo_name, format='JPEG', options={'quality': 60})

class Star(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    datetime = models.DateTimeField(auto_now_add=True)
