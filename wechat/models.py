from django.db import models
from api.models import *

# Create your models here.
class Wechat_user(models.Model):
    wechat_user = models.CharField(max_length=28, unique=True)
    hot_area = models.ForeignKey(Hot_area, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.wechat_user)

class Wechat_session(models.Model):
    wechat_user = models.ForeignKey(Wechat_user)
    datetime = models.DateTimeField(auto_now_add=True)
    query = models.TextField()

class Feedback(models.Model):
    wechat_user = models.ForeignKey(Wechat_user)
    content = models.TextField()

    def __unicode__(self):
        return unicode(self.wechat_user)

class Daily(models.Model):
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode(self.post.title)