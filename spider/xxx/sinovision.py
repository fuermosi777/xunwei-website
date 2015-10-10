# -*- coding: utf-8 -*-

from spider import tools

DOMAIN = 'http://www.sinovision.net'
URLS = ['http://www.sinovision.net/food.php']

def start():
    for url in URLS:
        title_list = get_title_list(url)
        for t in title_list:
            tools.store_post(get_post(t))

def get_title_list(page_url):
    return tools.get_list_from_page(page_url, selector='.module div.item_div a', attribute='href')

def get_post(url):
    soup = tools.get_soup(url)

    title = soup.select('h1.ph')[0].get_text()
    preview = soup.select('.s')[0].get_text()
    preview = preview[(preview.find(u'】')+1):preview.find('...')]
    body = soup.select('#article_content')[0]
    body = ''.join([unicode(x) for x in body.contents]) 

    try:
        page = soup.select('.pg label span')[0]['title']
        page = [int(s) for s in page.split() if s.isdigit()][0]
    except:
        page = None

    if page:
        url = url + '&page=%s'
        for x in range(2, page+1):
            u = url%x
            soup_page = tools.get_soup(u)
            b = soup_page.select('#article_content')[0]
            b = ''.join([unicode(x) for x in b.contents]) 
            body = body + b

    body = tools.extract_images(DOMAIN, body)
    return {
        'title': title,
        'source': url,
        'preview': preview,
        'body': body,
    }