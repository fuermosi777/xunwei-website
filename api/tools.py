def get_business_json(b):
    return {
        'id': b.id,
        'name': b.name,
        'name2': b.name2,
        'lat': b.latitude,
        'lng': b.longitude,
        'photo': b.photo.url,
        'street': b.street1,
        'city': b.city.name,
        'state': b.city.state.name,
        'postcode': b.postcode.number,
        'tag': [{
            'name': t.name
        } for t in b.tag.all()]
    }