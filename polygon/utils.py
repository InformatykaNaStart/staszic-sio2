import requests
import time
import string
import random
import hashlib

from errors import PolygonException

LOGIN  = 'staszic-sio2'
KEY    = '56d43d4b2d2d927cd48d3d800f81f41ea3914969'
SECRET = '87919bb525eeef25927d53aa547879bfbd786170'
RANDOM_ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits

def generate_sig(method_name, data):
    flattened = sorted(list(data.items()))
    rnd = ''.join(random.choice(RANDOM_ALPHABET) for _ in range(6))
    to_sig = '{}/{}?{}#{}'.format(
            rnd,
            method_name,
            '&'.join('{}={}'.format(k, v) for k, v in flattened),
            SECRET)
    return rnd + hashlib.sha512(to_sig).hexdigest()


def make_request(method_name, data):
    url = 'https://polygon.codeforces.com/api/{}'.format(method_name)
    new_data = data.copy()
    new_data['apiKey'] = KEY
    new_data['time'] = str(int(time.time()))
    new_data['apiSig'] = generate_sig(method_name, new_data)

    request = requests.post(url, data=new_data)
    if request.status_code != 200:
        raise PolygonException('There were some problems during invoking method {}: Polygon returned non 200 status code'.format(method_name))
    return request

def make_polygon_request(method_name, **data):
    request = make_request(method_name, data)

    json = request.json()
    if json['status'] == 'FAILED':
        raise PolygonException('There were some problems during invoking method {}: {}'.format(method_name, json['comment']))
    else:
        return json['result']

def make_polygon_plain_request(method_name, **data):
    return make_request(method_name, data).text
