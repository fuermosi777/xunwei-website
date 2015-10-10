from spider import tools

DOMAIN = 'http://www.eatbigapple.com'
URLS = [
    'http://www.eatbigapple.com/chinese/page/1/',
    ]

def start():
    for url in URLS:
        title_list = get_title_list(url)
        for t in title_list:
            tools.store_post(get_post(t))

def get_title_list(page_url):
    return tools.get_list_from_page(page_url, selector='h2.post-title.entry-title a', attribute='href')

def get_post(url):
    soup = tools.get_soup(url)

    title = soup.select('.post-title.entry-title a')[0].get_text()
    body = soup.select('.entry-content')[0]
    preview = body.get_text()[:400]
    body = ''.join([unicode(x) for x in body.contents]) 
    body = tools.extract_images(DOMAIN, body)
    return {
        'title': title,
        'source': url,
        'preview': preview,
        'body': body,
    }