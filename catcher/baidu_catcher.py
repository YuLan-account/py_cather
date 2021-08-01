import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
import time

from helper import file_helper
from setting import baidu_links_file, baidu_page_dir


class baidu_catcher:
    base_url = 'https://www.baidu.com/s?'
    wd = ''
    params = {
        "wd": '',
        'pn': 0,
        'rsv_spt': 1,
        'rsv_iqid': '0x91ab122f0004d53a',
        'issp': 1,
        'f': 8,
        'rsv_bp': 1,
        'rsv_idx': 2,
        'ie': 'utf-8',
        'rsv_enter': 1,
        'rsv_dl': 'tb',
        'rsv_sug3': 14,
        'rsv_sug1': 1,
        'rsv_sug4': 4122,
        'rsv_sug7': 100,
        'rsv_sug2': 0,
        'rsv_btype': 'i',
        'rsp': 6,
        'inputT': 3810
    }
    max_page = 1

    headers = {
        'Host': 'cstm.baidu.com',
        'Connection': 'Upgrade',
        'Pragma':'cache no',
        'Cache-Control': 'no-cache',
        'Upgrade': 'websocket',
        'Origin': 'https://www.baidu.com',
        # 'Sec-WebSocket-Version': 13,
        # 'Sec-WebSocket-Key': '0V5sJ85ztHiwbr62oyB63w==',
        # 'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": 'zh-CN,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }

    target_file = open(baidu_links_file, 'a')  # write append
    worker_count = 1

    def __init__(self, keyword, max_page, worker_count):
        self.wd = keyword
        self.max_page = max_page
        self.worker_count = worker_count

    def get_page_links(self, page_index):
        self.params['page'] = page_index
        self.params['wd'] = self.wd
        response = requests.get(url=self.base_url, headers=self.headers, params=self.params, allow_redirects=False)
        return response.content.decode()


    def filter_url(self, link):
        res = ""
        if link is not None and link.startswith('http://www.baidu.com/link?'):
            res = link
        return res

    def handle_page_and_store_to_file(self, link_set):
        for link in link_set:
            self.target_file.write(link + '\n')
        self.target_file.flush()

    def catch_links(self):
        for page_index in range(0, self.max_page):
            print(f' ============== 第 {page_index} 次爬取数据 ============== ')
            time.sleep(0.1)
            web_page = self.get_page_links(page_index)

            url_set = set([])
            soup = BeautifulSoup(web_page, 'html.parser')
            a_list = soup.findAll('a')
            for aElement in a_list:
                a_href = aElement.get('href')
                url_set.add(self.get_page_links(a_href))

            print('\n'.join(url_set))
            self.handle_page_and_store_to_file(url_set)

    def catch_content_from_url(self, url):
        page = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        contents = soup.find_all('p')
        all_content = ""
        for content in contents:
            all_content += (content.get_text())

        return all_content

    """
    存储爬下来的搜索链接
    """
    links = []
    file_name_index = 0
    file_index_lock = Lock()
    file_prefix = 'baidu_page_'
    file_suffix = '.txt'

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
                file_helper.save_page_to_file(dir=baidu_page_dir, page=page, filename=filename)
            except:
                print(f'catch content error filename: {filename}')


    """
    多线程处理
    """
    def start_multi_thread(self):
        if len(self.links) == 0:
            self.links = file_helper.load_all_url_from_file(baidu_links_file)
        if len(self.links) == 0:
            print('there is no links now !!! ')
            return

        """
        多线程处理
        """
        threads = []
        for thread_index in range(0, self.worker_count):
            thread = Thread(name=f'thread_{thread_index}', target=self.handle_page_from_url)
            threads.append(thread)

        for thread in threads:
            thread.start()


# 入口
if __name__ == '__main__':
    baidu_catcher = baidu_catcher(keyword='intitle: 农业视频会议 县', max_page=1, worker_count=5)
    baidu_catcher.catch_links()
    # baidu_catcher.start_multi_thread()