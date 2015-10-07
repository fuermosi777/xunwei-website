def get_business_json(b):
    return {
        'id': b.id,
        'name': b.name,
        'name2': b.name2,
        'lat': b.latitude,
        'lng': b.longitude,
        'phone': b.phone,
        'photo': b.photo.url,
        'street': b.street1,
        'city': b.city.name,
        'state': b.city.state.name,
        'postcode': b.postcode.number,
        'hot_area': b.hot_area.name,
        'tag': [{
            'name': t.name
        } for t in b.tag.all()]
    }

import qrcode
import base64
import cStringIO
def url_to_qrcode(url):
    img = qrcode.make(url)
    buffer = cStringIO.StringIO()
    img.save(buffer)
    img_str = base64.b64encode(buffer.getvalue())
    return img_str