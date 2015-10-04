#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django import template
from django.utils.translation import ugettext, ungettext
import pytz

register = template.Library()


@register.filter(name='timesince_human')
def humanize_timesince(date):
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