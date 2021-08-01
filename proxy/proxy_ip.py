import requests

from setting import proxy_url


def get_random_proxy_ip():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxy_url).text.strip()