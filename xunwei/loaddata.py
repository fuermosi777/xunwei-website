import json
from app.models import *
import urllib2
import urllib
from urlparse import urlparse
from django.core.files import File
from django.core.files.base import ContentFile
import decimal 
json_data = open('/home/fuermosi777/webapps/xunwei/xunwei/xunwei/items1.json')
data = json.load(json_data)
json_data.close()
cate = Category.objects.get(id=3)
for d in data:
    try:
        rr = Restaurant.objects.get(name=d['name'])
    except:
        try:
            state = State.objects.get(state=d['state'])
        except:
            state = State(state=d['state'])
            state.save()
        try:
            city = City.objects.get(name=d['city'])
        except:
            city = City(city=d['city'],state=state)
            city.save()
        try:
            postcode = Postcode.objects.get(postcode=d['postcode'])
        except:
            postcode = Postcode(postcode=d['postcode'],state=state)
            postcode.save()
        try:
            d['photo']
        except:
            d['photo'] = 'http://xun-wei.com/static/img/restaurant_default.jpg'
        f = open('temp.jpg','wb')
        f.write(urllib.urlopen(d['photo']).read())
        f.close()
        s = File(open('temp.jpg', 'r'))
        restaurant = Restaurant(name=d['name'],phone=d['phone'],street1=d['street'],city=city,postcode=postcode,photo=s,latitude=d['latitude'],longitude=d['longitude'],description=d['description'])
        try:
            restaurant.name2 = d['name2']
        except:
            pass
        restaurant.save()
        for s in d['subcategory']:
            try:
                sub = Subcategory.objects.get(name=s)
            except:
                sub = Subcategory(name=s,category=cate)
                sub.save()
            restaurant.subcategory.add(sub)
            restaurant.save()