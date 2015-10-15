from spider import tools

DOMAIN = 'http://wacowsf.com'
URLS = [
    'http://wacowny.com/category/restaurants-%E9%A4%90%E5%BB%B3%E6%8E%A8%E8%96%A6/?variant=zh-hans',
    'http://wacowsf.com/category/restaurants-%E9%A4%90%E5%BB%B3%E6%8E%A8%E8%96%A6/?variant=zh-hans',
    'http://wacowla.com/blog/category/all-restaurants/?variant=zh-hans']

def start():
    for url in URLS:
        print url
        title_list = get_title_list(url)
        for t in title_list:
            try:
                tools.store_post(get_post(t))
            except:
                print 'Storing %s is error'%t

def get_title_list(page_url):
    return tools.get_list_from_page(page_url, selector='h2.post-title a', attribute='href')

def get_post(url):
    soup = tools.get_soup(url)

    title = soup.select('h1.post-title a')[0].get_text()

    body = soup.select('.entry')[0]
    preview = body.get_text()[:80]

    body = ''.join([unicode(x) for x in body.contents]) 
    body = tools.extract_images(DOMAIN, body)
    return {
        'title': title,
        'source': url,
        'preview': preview,
        'body': body,
    }