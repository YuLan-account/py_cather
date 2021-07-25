import time

from analyze.content_catcher import  catch_content_from_sogou_url
from threading import Thread, Lock
import _thread
import os

file_prefix = 'sogou_page_'
file_suffix = '.txt'
file_name_index = 0

lock = Lock()

urls = []

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


def save_page_to_file(page, name):
    page_file = open(f'/Users/bytedance/PycharmProjects/pachong/text/article_sogou/{name}', 'w')
    page_file.write(page)
    page_file.flush()


def load_all_url_from_file(filename):
    if os.path.exists(filename) is False:
        print(f'{filename}  file not exists')
        return
    file = open(filename, 'r')
    urls = file.readlines()
    res = []
    for url in urls:
        new_url = url.strip('\n')
        if new_url != "":
            res.append(new_url)
    return res


def print_index():
    while True:
        global file_name_index
        time.sleep(0.2)
        with lock:
            file_name_index += 1
            print(f"thread name : {Thread.name}  index: {file_name_index}")


def handle_page_from_url():
    global file_name_index
    while file_name_index < len(urls):
        with lock:
            print(f'thread: {Thread.name} 正在处理第 {file_name_index} 篇文章')
            url = urls[file_name_index]
            file_name_index += 1
            filename = file_prefix + f'{file_name_index}' + file_suffix

        print(f'url: {url}')
        try:
            content = catch_content_from_sogou_url(url, headers)
            save_page_to_file(content, filename)
            print(f'filename: {filename} save success')
        except:
            print('unknown error')




if __name__ == '__main__':
    urls = load_all_url_from_file('/Users/bytedance/PycharmProjects/pachong/text/sogou.txt')
    try:
        thread_01 = Thread(target=handle_page_from_url)
        thread_02 = Thread(target=handle_page_from_url)
        thread_03 = Thread(target=handle_page_from_url)
        thread_04 = Thread(target=handle_page_from_url)
        thread_05 = Thread(target=handle_page_from_url)
        thread_06 = Thread(target=handle_page_from_url)
        thread_01.start()
        thread_02.start()
        thread_03.start()
        thread_04.start()
        thread_05.start()
        thread_06.start()
    except:
        print("Error: 无法启动线程")
