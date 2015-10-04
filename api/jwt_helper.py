import jwt

from secret import JWT_SECRET

def encode(stuff):
    return jwt.encode(stuff, JWT_SECRET, algorithm='HS256')

def decode(encoded):
    return jwt.decode(encoded, JWT_SECRET, algorithm=['HS256'])