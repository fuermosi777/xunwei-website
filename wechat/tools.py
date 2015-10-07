import hashlib
from secret import WECHAT_TOKEN

def check_signature(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)

    token = WECHAT_TOKEN

    temp_list = [token, timestamp, nonce]
    sorted_list = sorted(temp_list)
    temp_list = ''.join(sorted_list)
    temp_list = hashlib.sha1(temp_list)

    if temp_list.hexdigest() == signature:
        return True
    else:
        return False