import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import ssl
import sys
import time

url = 'https://www.baidu.com/s?'

regex1 = '农业视频会议'
regex2 = '县'

target_file = open('../text/baidu.txt', 'a')

def get_page(page_index):
    params = {
        "wd": "intitle: 农业视频会议 县",
        'pn': page_index * 10,
        'rqlang': 'cn',
        'rsv_enter': 0,
        'rsv_dl': 'tb',
        'rsv_btype': 't',
        'rsv_sug3': 50,
        'rsv_sug1': 18,
        'rsv_sug7': 100,
        'inputT': 769,
        'rsv_sug4': 6285
    }
    page = requests.get(url=url, headers=headers, params=params)
    if page.status_code == 200:
        return page.content.decode()


def filter_url(link):
    res = ""
    if link is not None and link.startswith('http://www.baidu.com/link?'):
        res = link
    return res


def handle_page_and_store_to_file(link_set):
    for link in link_set:
        target_file.write(link + '\n')
    target_file.flush()


if __name__ == '__main__':
    for page_index in range(0, 49):
        print(f' ============ 第{page_index}次爬取 ============ ')
        content = get_page(page_index)
        url_set = set([])
        soup = BeautifulSoup(content, 'html.parser')
        a_list = soup.findAll('a')
        for aElement in a_list:
            a_href = aElement.get('href')
            url_set.add(filter_url(a_href))

        # res_str = '\n'.join(url_set)
        # print(res_str)
        handle_page_and_store_to_file(url_set)
