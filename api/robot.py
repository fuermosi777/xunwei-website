from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import *
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as BS
import urllib2
from urlparse import urlparse, parse_qsl
import uuid
import mimetypes
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

@csrf_exempt
def post(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    business_id = request.POST.get('business_id', None)
    url = request.POST.get('url', None)
    title = request.POST.get('title', None)
    preview = request.POST.get('preview', None)

    if None in (business_id, url, title, preview):
        return HttpResponse(status=500)

    business = Business.objects.get(id=business_id)

    post = Post(
        title=title,
        preview=preview,
        body=' ',
        source=url,
        business=business,
        is_approved=True,
    )

    post.save()
    try:
        post.save()
    except:
        pass

    res = {}
    return JsonResponse(res, safe=False)

@csrf_exempt
def business(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    url = request.POST.get('url', None)
    name2 = request.POST.get('name2', '') # optional
    tag = request.POST.get('tag', None)
    hot_area = request.POST.get('hot_area', None)
    photo_url = request.POST.get('photo_url', None)

    page = urllib2.urlopen(url).read()
    soup = BS(page)

    name = soup.find('h1', {'class': 'biz-page-title'}).get_text().lstrip()
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
        print q[0]
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

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding': 'none',
        # 'Accept-Language': 'en-US,en;q=0.8',
        # 'Connection': 'keep-alive',
        'referer': 'http://www.yelp.com/',
    }

    ext = mimetypes.guess_extension(mimetypes.guess_type(photo_url)[0])
    req = urllib2.Request(photo_url, headers=headers)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib2.urlopen(req).read())
    img_temp.flush()

    business.photo.save('%s%s'%(uuid.uuid4(), ext), File(img_temp))
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

    # store image
    res = {}
    return JsonResponse(res, safe=False)