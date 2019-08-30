from collections import OrderedDict
from urllib.parse import urlencode

def order_list_api(request, data, page, max_per_page, total):
    """ 顺序展示返回结果, 像Django DRF一样的返回。
    :param request:
    :param data:
    :param page:
    :param max_per_page:
    :param total:
    :return:
    """

    url_urlencode = get_urlencode(request)
    cur_count = max_per_page * page
    # host = "{}://{}".format(request.scheme, request.host)
    host = "http://192.168.1.24:6070"
    previous_url = next_url = None
    if total > cur_count:
        next_url = '{}{}?page={}'.format(host, request.path, page + 1)
        next_url = add_urlencode_to_url(next_url, url_urlencode)
    if cur_count > max_per_page:
        previous_url = '{}{}?page={}'.format(host, request.path, page - 1)
        previous_url = add_urlencode_to_url(previous_url, url_urlencode)
    return OrderedDict([
        ('count', total),
        ('next', next_url),
        ('previous', previous_url),
        ('results', data)
    ])

def get_urlencode(request):
    args = request.args
    url_args = {k: args.get(k) for k, v in args.items()}
    if 'page' in url_args:
        del url_args['page']
    url_urlencode = urlencode(url_args)
    return url_urlencode

def add_urlencode_to_url(url, url_urlencode):
    if url_urlencode:
        url = "{}&{}".format(url, url_urlencode)
    return url