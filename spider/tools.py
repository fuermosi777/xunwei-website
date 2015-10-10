from bs4 import BeautifulSoup as BS
import urllib2
from api.models import *
from urlparse import urlparse, urljoin
import uuid, os
import mimetypes
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    }
    request = urllib2.Request(url, headers=headers)
    page = urllib2.urlopen(request)
    soup = BS(page.read())
    return soup

def get_list_from_page(url, selector, attribute):
    soup = get_soup(url)
    res = []
    select = soup.select(selector)
    for s in select:
        res.append(s[attribute])
    return res

def get_items_from_page(url, selector_dict):
    soup = get_soup(url)
    res = {}
    for key, value in selector_dict.iteritems():
        select = soup.select(value['selector'])
        if value['attribute'] == 'get_text':
            res[key] = select.get_text()
        else:
            res[key] = soup.select(value['selector'])[value['attribute']]
    return res

def store_post(dict):
    try:
        post = Post.objects.get(title=dict['title'])
    except:
        post = Post(title=dict['title'],
            preview=dict['preview'],
            source=dict['source'],
            body=dict['body'],
            business_id=56,
            is_approved=False,
        )
        post.save()
        print post.title
    return 

def url_add_pre(pre, url):
    # turn url such as '/xxx.jpg' to 'http://aa.com/xxx.jpg'
    parse_res = urlparse(url)
    if not parse_res.netloc:
        return urljoin(pre, url)
    else:
        return url

def extract_images(domain, body):
    soup = BS(body)
    [tag.extract() for tag in soup.select('h1')]
    [tag.extract() for tag in soup.select('.meta')]
    [tag.extract() for tag in soup.select('p.tags')]
    [tag.extract() for tag in soup.select('p.cats')]
    for tag in soup():
        for attribute in ["class", "id", "name", "style", "width", "height", "color"]:
            del tag[attribute]

    for img in soup.findAll('img'):
        img_src = url_add_pre(domain, img['src'])
        img['src'] = img_src
        #img['src'] = store_post_image_from_url(domain, img_src)
    return unicode(soup)

def store_post_image_from_url(domain, image_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding': 'none',
        # 'Accept-Language': 'en-US,en;q=0.8',
        # 'Connection': 'keep-alive',
        'referer': domain,
    }
    if urlparse(image_url).scheme == 'data':
        return image_url
    else:
        ext = mimetypes.guess_extension(mimetypes.guess_type(image_url)[0])
        request = urllib2.Request(image_url, headers=headers)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(request).read())
        img_temp.flush()

        post_photo = Post_photo()
        post_photo.photo.save('%s%s'%(uuid.uuid4(), ext), File(img_temp))
        post_photo.save()
        return post_photo.photo.url