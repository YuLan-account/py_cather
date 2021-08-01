import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
import time
import re

from helper import file_helper
from helper.string_helper import isBlank, isNotBlank
from proxy.proxy_ip import get_random_proxy_ip
from setting import sogou_links_file, sogou_page_dir, sogou_cookie


class Element:
    title: ''
    link: ''

    def __init__(self, title, link):
        self.title = title
        self.link = link

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



    target_file = open(sogou_links_file, 'a')  # write append
    cookie = ""  # 登录之后的cookie
    max_page = 1  # 最大抓取页数

    def __init__(self, max_page, keyword):
        print('sogou catcher init ....')
        self.headers['Cookie'] = sogou_cookie
        self.max_page = max_page
        self.keyword = keyword


    @staticmethod
    def format_sogou_url(link, title):
        if link is not None and isNotBlank(title) and link.startswith('/link?') and link.find('dn9a') != -1:
            res_link = title + "|" + "https://weixin.sogou.com" + link
            print(res_link)
            return res_link
        return ""


    """
    获取搜索页的跳转链接
    """
    def get_web_page_list(self, page):
        try:
            proxy_ip = get_random_proxy_ip()
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

        # try:
        response = requests.get(url=self.base_url, headers=self.headers, params=params, proxies=proxies,
                                allow_redirects=False)
        if response.status_code == 200:
            return response.content.decode()
        if response.status_code == 302:  # 反爬生效，状态码错误
            print(response.content.decode())
            proxy_ip = get_random_proxy_ip()
            if proxy_ip:
                print('use proxy', proxy_ip)
                return self.get_web_page_list(page)  # 当代理池的公开ip被占用，此处会循环获取直至有可用ip
            else:
                print('get page with get proxy error')
                return None
        # except:
        #     print('请求失败，开始重试')
        #     self.get_web_page_list(page)

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
                text = aElement.text

                url_set.add(self.format_sogou_url(a_href, text))

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

    def handle_page_from_url(self):
        while self.file_name_index < len(self.links):
            time.sleep(0.2)
            with self.file_index_lock:
                print(f'thread: {Thread.name} 正在处理第 {self.file_name_index} 篇文章')
                article_url = self.links[self.file_name_index].split('|')
                title = article_url[0]
                link = article_url[1]
                self.file_name_index += 1
                filename = "{}{}{}".format(self.file_prefix, self.file_name_index, self.file_suffix)

            print(f'>>>>>>> current filename: {filename}, link: {link}')
            try:
                page = self.catch_content_from_sogou_url(link)
                page = title + '\n' + page
                print(page)
                file_helper.save_page_to_file(dir=sogou_page_dir, page=page, filename=filename)
            except:
                print(f'catch content error filename: {filename}')

    """
    多线程处理
    """
    def start_multi_thread(self, thread_count):
        if len(self.links) == 0:
            self.links = file_helper.load_all_url_from_file(sogou_links_file)
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
    sogou_catcher = sogou_catcher(max_page=100, keyword='村务公开信息平台 县')
    sogou_catcher.catch_link()
    # sogou_catcher.start_multi_thread(thread_count=10)


