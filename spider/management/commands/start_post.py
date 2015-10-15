# -*- coding: utf-8 -*-

import sys
from django.core.management.base import BaseCommand, CommandError
from api.models import *
from datetime import datetime, timedelta
from multiprocessing import Pool
from django.db import connection
import importlib
from bs4 import BeautifulSoup as BS
import urllib2
from urlparse import urlparse, parse_qsl
import uuid
import mimetypes
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class Command(BaseCommand):
    help = ""
    args = '<test>'
    def handle(self, *args, **options):
        post = Post.objects.filter(hide=False, source__icontains='http://chihuo.org/', is_approved=False)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            # 'Accept-Encoding': 'none',
            # 'Accept-Language': 'en-US,en;q=0.8',
            # 'Connection': 'keep-alive',
            'referer': 'http://www.yelp.com/',
        }
        for p in post:
            name = p.source.replace('http://chihuo.org/', '')
            name = name.replace('/', '')
            name = name.replace('-', '+')
            keyword = name + '+LA+yelp'
            google_url = 'https://www.google.com/search?q=%s'%keyword

            google_soup = BS(urllib2.urlopen(urllib2.Request(google_url, headers=headers)).read())
            urls = google_soup.select('h3.r a')
            yelp_url = None
            for u in urls:
                if 'yelp.com' in u['href']:
                    yelp_url = u['href']
                    break
            if not yelp_url:
                print 'Not found YELP'
                yelp_url = raw_input('Enter Yelp link: ')

            hot_area = '洛杉矶'
            soup = BS(urllib2.urlopen(urllib2.Request(yelp_url, headers=headers)).read())

            name = soup.find('h1', {'class': 'biz-page-title'}).get_text().lstrip().rstrip()
            print name
            name2 = raw_input('Enter Chinese name if has: ')

            tags = soup.find('span', {'class': 'category-str-list'}).get_text()
            print tags
            tag = raw_input('Enter tags: ')
            if not tag:
                return

            phone = soup.find('span', {'class': 'biz-phone'}).get_text()
            phone = ''.join([s for s in phone if s.isdigit()])
            street1 = soup.find('span', {'itemprop': 'streetAddress'}).get_text()
            city_text = soup.find('span', {'itemprop': 'addressLocality'}).get_text()
            state_text = soup.find('span', {'itemprop': 'addressRegion'}).get_text()
            postcode_text = soup.find('span', {'itemprop': 'postalCode'}).get_text()
            map_url = soup.select('a.biz-map-directions img')[0]['src']
            query = urlparse(map_url).query
            query_parsed = parse_qsl(query)
            lat = None
            lng = None
            for q in query_parsed:
                if q[0] == 'center':
                    center = q[1]
                    lat = center.split(',')[0]
                    lng = center.split(',')[1]

            try:
                state = State.objects.get(name=state_text)
            except:
                state = State(name=state_text)
                state.save()

            try:
                city = City.objects.get(name=city_text)
            except:
                city = City(name=city_text, state=state)
                city.save()

            try:
                postcode = Postcode.objects.get(number=postcode_text)
            except:
                postcode = Postcode(number=postcode_text, state=state)
                postcode.save()

            try:
                hot_area = Hot_area.objects.get(name=hot_area)
            except:
                hot_area = hot_area(name=hot_area)
                hot_area.save()

            business = Business(
                name=name,
                name2=name2,
                phone=phone,
                street1=street1,
                city=city,
                postcode=postcode,
                latitude=lat,
                longitude=lng,
                hot_area=hot_area,
            )

            photo_url = soup.select('.showcase-photo-box img')[0]['src']
            ext = mimetypes.guess_extension(mimetypes.guess_type(photo_url)[0])
            req = urllib2.Request(photo_url, headers=headers)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(req).read())
            img_temp.flush()

            business.photo.save('%s%s'%(uuid.uuid4(), ext), File(img_temp))
            print '--- 确定吗? ---'
            print p.title, business.name, business.name2
            sure = raw_input('确定吗？')
            if sure in ['y', 'Y', 'yes', 'YES', 'Yes']:
                business.save()
                # tag
                tag = tag.split(' ')
                for t in tag:
                    try:
                        t_instance = Tag.objects.get(name=t)
                    except:
                        t_instance = Tag(name=t)
                        t_instance.save()
                    business.tag.add(t_instance)

                p.hide = True
                p.business = business
                p.save()
                print 'Succuess'
            else:
                print 'Fail'