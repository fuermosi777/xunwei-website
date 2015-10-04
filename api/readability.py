import urllib2, json

TOKEN = 'b012a3964a15e0a1c2d6376aefee0ee60fa5656e'

PARSER_URL = 'https://readability.com/api/content/v1/parser?token=%s&url=%s'

def read_from_url(url):
    url = url.encode('utf-8')
    target_url = PARSER_URL%(TOKEN, url)
    response = urllib2.urlopen(target_url)
    data = json.loads(response.read())
    return data