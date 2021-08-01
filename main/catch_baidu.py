import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import random
from setting import baidu_links_file
from proxy.proxy_ip import get_random_proxy_ip

url = 'https://www.baidu.com/s?'

wd = '县 行政审批 不见面审批'

headers = {
    # 'Host': "www.baidu.com",
    # 'Connection': "keep-alive",
    # 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    # 'is_xhr': 1,
    # 'sec-ch-ua-mobile': "?0",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    # 'is_pbs': "intitle%3A%20%E5%86%9C%E4%B8%9A%E8%A7%86%E9%A2%91%E4%BC%9A%E8%AE%AE%20%E5%8E%BF",
    # 'Accept': "*/*",
    # 'X-Requested-With': "XMLHttpRequest",
    # 'is_referer': "https://www.baidu.com/s?wd=intitle%3A%20%E5%86%9C%E4%B8%9A%E8%A7%86%E9%A2%91%E4%BC%9A%E8%AE%AE%20%E5%8E%BF&rsv_spt=1&rsv_iqid=0xe1a0d69f00095bd0&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_dl=tb&rsv_enter=0&oq=intitle%253A%2520%25E5%2586%259C%25E4%25B8%259A%25E8%25A7%2586%25E9%25A2%2591%25E4%25BC%259A%25E8%25AE%25AE%2520%25E5%258E%25BF&rsv_btype=t&rsv_t=f5d0jBCFKGkMVonNOwK5KTqYvkFTGr2X6SND0Qw57GROVBMzOhaaDLCtxA41M59d8u2j&rsv_pq=ede6de1c00034dcc&prefixsug=intitle%253A%2520%25E5%2586%259C%25E4%25B8%259A%25E8%25A7%2586%25E9%25A2%2591%25E4%25BC%259A%25E8%25AE%25AE%2520%25E5%258E%25BF&rsp=0&bs=intitle%3A%20%E5%86%9C%E4%B8%9A%E8%A7%86%E9%A2%91%E4%BC%9A%E8%AE%AE%20%E5%8E%BF",
    # 'Sec-Fetch-Site': "same-origin",
    # 'Sec-Fetch-Mode': "cors",
    # 'Sec-Fetch-Dest': "empty",
    # 'Referer': "https://www.baidu.com/s?wd=intitle%3A%20%E5%86%9C%E4%B8%9A%E8%A7%86%E9%A2%91%E4%BC%9A%E8%AE%AE%20%E5%8E%BF&rsv_spt=1&rsv_iqid=0xe1a0d69f00095bd0&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_dl=tb&rsv_enter=0&oq=intitle%253A%2520%25E5%2586%259C%25E4%25B8%259A%25E8%25A7%2586%25E9%25A2%2591%25E4%25BC%259A%25E8%25AE%25AE%2520%25E5%258E%25BF&rsv_btype=t&rsv_t=48e1LsKbglXVuKSz9Um6xwr86hTi%2BczUty4npqzf1K0q0IL5%2B43PJ%2FFA7WMXqGvv%2FBHm&rsv_pq=ee19dce500003af0&prefixsug=intitle%253A%2520%25E5%2586%259C%25E4%25B8%259A%25E8%25A7%2586%25E9%25A2%2591%25E4%25BC%259A%25E8%25AE%25AE%2520%25E5%258E%25BF&rsp=0",
    # 'Accept-Encoding': "gzip, deflate, br",
    # 'Accept-Language': "zh-CN,zh;q=0.9",
    # 'Cookie': "BIDUPSID=ACF04FC99EA4DCD4D324FCE029E59FEF; PSTM=1619788321; BAIDUID=ACF04FC99EA4DCD42A99149CCC1C7CD8:FG=1; BD_UPN=123253; __yjs_duid=1_275039f9a41d5e5ddfa02f82fc13e72d1619850787113; BDUSS=U00OGozS0xRaX41TUVMTEU1VWdFTy1XalVBfjVxWmNmekE1djNUbEZhV1ItYlpnRVFBQUFBJCQAAAAAAAAAAAEAAACngqDHWXVMYW5Hb28AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJFsj2CRbI9gT; BDUSS_BFESS=U00OGozS0xRaX41TUVMTEU1VWdFTy1XalVBfjVxWmNmekE1djNUbEZhV1ItYlpnRVFBQUFBJCQAAAAAAAAAAAEAAACngqDHWXVMYW5Hb28AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJFsj2CRbI9gT; BDSFRCVID_BFESS=Qu0sJeCCxG3oG56eUk6lVzEK5ahEAXiar1N23J; H_BDCLCKID_SF_BFESS=tJKO_I_bJK-3h4-C2DTV2t0e5UIX5-RLfbnnbp7F5l8-h432jtQV-PQBbf5R5qKLMmjj_nv_0JrxOKQphpQYhhIVDJPtK4oRaD5Q5xcN3KJmVPP9bT3vj-Dt2h6q2-biWb7M2MbdJpbP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhbLGe6-aD6vbDaD8q-J3-DOL06rtMROsHt5kbITjh6PEXpo9BtQmJJrL2qQbBKOqMR5P5P54qJFIbnQuKq-fQg-q3RAa2-QVhqPGhhjbKl-7KlJB0x-jLT7OVn0MW-5DfJocDtnJyUnybPnnBT3R3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CFhf-JHD6rP-trf5DCShUFsKtvdB2Q-XPoO3K8WbK3FbtcCXttV3mc8W43wKHTbQfbgylRpDfjSyM6OLlkkBURpBtQmJeTxoUJ2-KDVeh5Gqfo15-0ebPRiJ-b9Qg-JKpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hDICe5_5j65M5MtXanJJHD7yWCvgaT6cOR5Jj65bQlDpbx5-L4Pq5ejzbPK-5lkK8PoO3MA--t4q0xQbWfJfQ55qb4cYJh3msq0x0-jte-bQypoa0P5ztKOMahkb5h7xOKbMQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTLeHDOt6tqJJ3J05rS---_Hn7zeT5jeM4pbt-qJJblLeQh3J5G2KQr8fcM5j5qyTDgK4nnBT5Ka5T7M-5vKKJsqMQC2xubQp8kQN3TKtKO5bRiLRog5fF5Dn3oyTbJXp0njb3ly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJCsB4OVbnK_HRjYbb__-P4DenQtJnJZ5m7mXp0bah0hMR5aMTjS3RIkyNoKaUQCyI5KQDjktDOkbRO4-TFhjTbXDf5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=34300_34099_34335_31253_34375_34004_34283_34293_34111_26350_34246; ab_sr=1.0.1_MjJhZTFkZTU2NGQ3YWUwYTZiMDJkYTkwM2RhYWRhNzFhMDA5MzA5Njk1Y2E2NzY5YjgxOTQ2YmNjNjliNzBlZmM5OTdmMTFkNzY1NzMxY2MxMzczZGNhNTNkMDYzOTg5YmIyODE1YWNmYTkzNDk1ZjUxMGM0MGU2MjkwZWM1MGExZDUzMTVmOTJlYjA3ZWNkNWU4ZTJiYmEyNzJjMGEzOGM4MzdjMTcyNDE0ZWMzODcxODJmMDVkYzZiNGU5ZWFi; delPer=0; BD_CK_SAM=1; PSINO=6; BAIDUID_BFESS=ACF04FC99EA4DCD42A99149CCC1C7CD8:FG=1; H_PS_645EC=48e1LsKbglXVuKSz9Um6xwr86hTi%2BczUty4npqzf1K0q0IL5%2B43PJ%2FFA7WMXqGvv%2FBHm; BA_HECTOR=ak80242ga4a52l21mb1ggb1500q; BDSVRTM=334; WWW_ST=1627751586472"
}

target_file = open(baidu_links_file, 'a')


class Element:
    title = ''
    link = ''

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __repr__(self):
        return '<Element {}>'.format(self.name)


def get_page(page_index):
    params = {
        "wd": wd,
        'pn': (page_index - 1) * 10,
        # 'lm': 1,
        # 'rsv_spt': 1,
        # 'rsv_iqid': '0x91ab122f0004d53a',
        # 'issp': 1,
        # 'f': 8,
        # 'rsv_bp': 1,
        # 'rsv_idx': 2,
        # 'ie': 'utf-8',
        # 'rsv_enter': 1,
        # 'rsv_dl': 'tb',
        # 'rsv_sug3': 14,
        # 'rsv_sug1': 1,
        # 'rsv_sug4': 4122,
        # 'rsv_sug7': 100,
        # 'rsv_sug2': 0,
        # 'rsv_btype': 'i',
        # 'rsp': 6,
        # 'inputT': 3810
    }
    # proxy_ip = get_random_proxy_ip()
    # proxies = {'http': 'http://' + proxy_ip}  # 使用该ip访问

    response = requests.get(url=url, headers=headers, params=params)
    print(response.content)

    return response.content.decode()
    # if response.status_code == 200:
    #     return response.content.decode()
    # if response.status_code == 302:  # 反爬生效，状态码错误
    #     proxy_ip = get_random_proxy_ip()
    #     if proxy_ip:
    #         print('use proxy', proxy_ip)
    #         return get_page(page_index)  # 当代理池的公开ip被占用，此处会循环获取直至有可用ip
    #     else:
    #         print('get page with get proxy error')
    #         return None


def filter_url_and_title(aElement, link):
    if link is not None and link.startswith('http://www.baidu.com/link?'):
        title = aElement.text
        return Element(link=link, title=title)
    else:
        return None


def isBlank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return False
        # myString is None OR myString is empty or blank
    return True


def handle_page_and_store_to_file(element_set):
    for element in element_set:
        if not isBlank(element.title):
            print(f'{element.title} | {element.link}')
            target_file.write(element.title + "|" + element.link + '\n')
    target_file.flush()


if __name__ == '__main__':
    # while True:
    # sleep_time = random.randint(3, 7)
    # time.sleep(int(sleep_time))
    # print(f'第{index}次抓取')
    for index in range(0, 50):
        print(f'第{index}次抓取')
        content = get_page(4)
        element_set = set([])
        soup = BeautifulSoup(content, 'html.parser')
        a_list = soup.findAll('a')
        for aElement in a_list:
            a_href = aElement.get('href')

            element = filter_url_and_title(aElement, a_href)
            if element is not None:
                element_set.add(element)

        handle_page_and_store_to_file(element_set)

        print(f'已完成第{index}次抓取')
        index += 1

