import re

from importlib import import_module
from urllib.parse import urlparse, unquote


def import_class(string):

    parts = string.split('.')

    cls = parts.pop()

    module = import_module('.'.join(parts))

    return getattr(module, cls)


def format_url(url, protocol='http'):

    if url.startswith(protocol) is False:
        if url.startswith('://') is True:
            url = f'{protocol}{url}'
        else:
            url = f'{protocol}://{url}'

    return unquote(url)


def get_domain_from_url(url, with_www=True):

    url = format_url(url)
    url = urlparse(url)

    domain = url.netloc

    if with_www is False:
        domain = re.sub(r'^www\.', '', domain)

    return domain


def get_path_from_url(url, starts_with_slash=True):

    url = format_url(url)
    url = urlparse(url)

    path = url.path.strip('/')

    if starts_with_slash is True:
        path = f'/{path}'

    return path


def get_query_string_from_url(url):

    url = format_url(url)
    url = urlparse(url)

    query_string = url.query
    if len(query_string) > 0:
        query_string = f'?{query_string}'

    return query_string
