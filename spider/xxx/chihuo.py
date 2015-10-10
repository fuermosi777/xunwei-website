from spider import tools

DOMAIN = 'http://chihuo.org'
URLS = ['http://chihuo.org/category/food-reviews/page/1/',
]

def start():
    for url in URLS:
        title_list = get_title_list(url)
        for t in title_list:
            tools.store_post(get_post(t))

def get_title_list(page_url):
    return tools.get_list_from_page(page_url, selector='article h2 a', attribute='href')

def get_post(url):
    soup = tools.get_soup(url)

    title = soup.select('h1.post-title.entry-title')[0].get_text()

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
