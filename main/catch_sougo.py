import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import sys
import ssl
import time

url = 'https://weixin.sogou.com/weixin?'

proxy_url = 'http://127.0.0.1:5555/random'  # 获取代理ip的端口

keyword ='农业视频会议 县'

headers = {
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept-Language": 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cache-Control': 'max-age=0',
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Cookie': 'ABTEST=0|1627100203|v1; IPLOC=CN4403; SUID=7E1388774842910A0000000060FB942B; SUID=7E1388771F49910A0000000060FB942B; weixinIndexVisited=1; SUV=00F9E6617788137E60FB942C9C96B467; JSESSIONID=aaaaLEjYZS1N49gRmf_Ox; PHPSESSID=hvpptqr5sritvs68b7oplt8m10; SNUID=76148F70070DC0D82882A92208868454; ppinf=5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA; pprdig=QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo; ppinfo=e7428eb679; passport=5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA|8bc25f0a78|QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo; sgid=24-53059563-AWD8OPncjs8DsDmrMh4bV4o; ppmdig=1627181377000000ef90d3ac2b840a9abcf3e8d04545a3ee'
}

target_file = open('/Users/bytedance/PycharmProjects/pachong/text/sogou.txt', 'a')


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxy_url).text.strip()


def get_page(page):
    params = {
        'query': keyword,
        's_from': 'input',
        '_sug_': 'n',
        'type': 2,
        'page': page,
        'ie': 'utf8'
    }

    ssl._create_default_https_context = ssl._create_unverified_context
    proxy_ip = get_random_proxy()
    proxies = {'http': 'http://' + proxy_ip}  # 使用该ip访问
    try:
        response = requests.get(url=url, headers=headers, params=params, proxies=proxies, allow_redirects=False)
        if response.status_code == 200:
            return response.content.decode()
        if response.status_code == 302:  # 反爬生效，状态码错误
            proxy_ip = get_random_proxy()
            if proxy_ip:
                print('use proxy', proxy_ip)
                return get_page(url, params)  # 当代理池的公开ip被占用，此处会循环获取直至有可用ip
            else:
                print('get proxy error')
                return None
    except:
        print('unknown error')
        return None


def format_sogou_url(link):
    res = ""
    if link is not None and link.startswith('/link?') and link.find('S__Dp') != -1:
        res = "https://weixin.sogou.com" + link
        return res
    return ""


def handle_page_and_store_to_file(link_set):
    for link in link_set:
        target_file.write(link + '\n')
    target_file.flush()


if __name__ == '__main__':
    for page_index in range(1, 101):
        print(f' ============== 第 {page_index} 次爬取数据 ============== ')
        time.sleep(0.1)
        content = get_page(page_index)
        url_set = set([])
        soup = BeautifulSoup(content, 'html.parser')
        a_list = soup.findAll('a')
        for aElement in a_list:
            a_href = aElement.get('href')
            url_set.add(format_sogou_url(a_href))

        res_str = '\n'.join(url_set)
        print(res_str)
        handle_page_and_store_to_file(url_set)

