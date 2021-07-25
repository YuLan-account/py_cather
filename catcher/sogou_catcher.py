import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
import _thread
import time
import re
import os

from setting import proxy_url, sogou_links_file, sogou_page_dir


class sogou_catcher:
    """
    负责抓取搜狗微信
    """
    base_url = 'https://weixin.sogou.com/weixin?'
    keyword = ""
    headers = {
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cache-Control': 'max-age=0',
        "Connection": "keep-alive",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        'Cookie': ''
    }

    target_file_dir = ''
    target_file = open(sogou_links_file, 'a')  # write append
    cookie = ""  # 登录之后的cookie
    max_page = 1  # 最大抓取页数

    def __init__(self, cookie, max_page, keyword):
        print('sogou catcher init ....')
        self.cookie = cookie
        self.headers['Cookie'] = self.cookie
        self.max_page = max_page
        self.keyword = keyword

    @staticmethod
    def get_random_proxy_ip():
        """
        get random proxy from proxypool
        :return: proxy
        """
        return requests.get(proxy_url).text.strip()

    @staticmethod
    def format_sogou_url(link):
        if link is not None and link.startswith('/link?') and link.find('S__D') != -1:
            res = "https://weixin.sogou.com" + link
            return res
        return ""

    """
    获取搜索页的跳转链接
    """

    def get_web_page_list(self, page):
        try:
            proxy_ip = self.get_random_proxy_ip()
            proxies = {'http': 'http://' + proxy_ip}  # 使用该ip访问

        except:
            print('请检查是否打开proxy pool')

        params = {
            'query': self.keyword,
            's_from': 'input',
            '_sug_': 'n',
            'type': 2,
            'ie': 'utf8',
            'page': page
        }

        print(f' params : {params}')

        response = requests.get(url=self.base_url, headers=self.headers, params=params, proxies=proxies,
                                allow_redirects=False)
        if response.status_code == 200:
            return response.content.decode()
        if response.status_code == 302:  # 反爬生效，状态码错误
            proxy_ip = self.get_random_proxy_ip()
            if proxy_ip:
                print('use proxy', proxy_ip)
                return self.get_web_page_list(self.params)  # 当代理池的公开ip被占用，此处会循环获取直至有可用ip
            else:
                print('get page with get proxy error')
                return None

    def handle_page_and_store_to_file(self, link_set):
        for link in link_set:
            self.target_file.write(link + '\n')
        self.target_file.flush()

    def catch_link(self):
        for page_index in range(0, self.max_page):
            print(f' ============== 第 {page_index} 次爬取数据 ============== ')
            time.sleep(0.1)
            web_page = self.get_web_page_list(page_index)
            url_set = set([])
            soup = BeautifulSoup(web_page, 'html.parser')
            a_list = soup.findAll('a')
            for aElement in a_list:
                a_href = aElement.get('href')
                url_set.add(self.format_sogou_url(a_href))

            print('\n'.join(url_set))
            self.handle_page_and_store_to_file(url_set)

    def catch_content_from_url(self, url):
        page = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        contents = soup.find_all('p')
        all_content = ""
        for content in contents:
            all_content += (content.get_text())

        print(f"all content: {all_content}")
        return all_content

    def catch_content_from_sogou_url(self, url):
        page = requests.get(url=url, headers=self.headers)
        js_text = page.text
        real_url = ''
        parts = re.findall(r'\+\=\ \'.+', js_text)

        for i in parts:
            real_url += i[4:-3]
        real_url.replace("@", "")
        print(f'real_url: {real_url}')
        return self.catch_content_from_url(real_url)

    """
    存储爬下来的搜索链接
    """
    links = []
    file_name_index = 0
    file_index_lock = Lock()
    file_prefix = 'sogou_page_'
    file_suffix = '.txt'

    @staticmethod
    def load_all_url_from_file():
        file = open(sogou_links_file, 'r')  # write append
        urls = file.readlines()
        res = []
        for url in urls:
            new_url = url.strip('\n')
            if new_url != "":
                res.append(new_url)
        return res

    @staticmethod
    def save_page_to_file(page, filename):
        page_file = open(f'{sogou_page_dir}/{filename}', 'w')
        page_file.write(page)
        page_file.flush()

    def handle_page_from_url(self):
        while self.file_name_index < len(self.links):
            with self.file_index_lock:
                print(f'thread: {Thread.name} 正在处理第 {self.file_name_index} 篇文章')
                link = self.links[self.file_name_index]
                self.file_name_index += 1
                filename = "{}{}{}".format(self.file_prefix, self.file_name_index, self.file_suffix)

            print(f'>>>>>>> current filename: {filename}, link: {link}')
            try:
                page = self.catch_content_from_sogou_url(link)
                self.save_page_to_file(page, filename)
            except:
                print(f'catch content error filename: {filename}')

    """
    多线程处理
    """

    def start_multi_thread(self, thread_count):
        if len(self.links) == 0:
            self.links = self.load_all_url_from_file()
        if len(self.links) == 0:
            print('there is no links now !!! ')
            return

        """
        多线程处理
        """
        threads = []
        for thread_index in range(0, thread_count):
            thread = Thread(name=f'thread_{thread_index}', target=self.handle_page_from_url)
            threads.append(thread)

        for thread in threads:
            thread.start()


if __name__ == '__main__':
    cookie = 'ABTEST=0|1627100203|v1; IPLOC=CN4403; SUID=7E1388774842910A0000000060FB942B; SUID=7E1388771F49910A0000000060FB942B; weixinIndexVisited=1; SUV=00F9E6617788137E60FB942C9C96B467; JSESSIONID=aaaaLEjYZS1N49gRmf_Ox; PHPSESSID=hvpptqr5sritvs68b7oplt8m10; SNUID=76148F70070DC0D82882A92208868454; ppinf=5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA; pprdig=QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo; ppinfo=e7428eb679; passport=5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA|8bc25f0a78|QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo; sgid=24-53059563-AWD8OPncjs8DsDmrMh4bV4o; ppmdig=16272256300000000a5f54c8b278a06571c9850155039a08'
    sogou_catcher = sogou_catcher(cookie=cookie, max_page=2, keyword='奥特曼')
    sogou_catcher.catch_link()
    sogou_catcher.start_multi_thread(thread_count=6)
