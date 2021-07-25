import time

from analyze.content_catcher import catch_content_from_url
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
    'Cookie': 'ABTEST=0|1627100203|v1; IPLOC=CN4403; SUID=7E1388774842910A0000000060FB942B; SUID=7E1388771F49910A0000000060FB942B; weixinIndexVisited=1; SUV=00F9E6617788137E60FB942C9C96B467; JSESSIONID=aaaaLEjYZS1N49gRmf_Ox; PHPSESSID=hvpptqr5sritvs68b7oplt8m10; SNUID=76148F70070DC0D82882A92208868454; ppinf=5|1627142284|1628351884|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIyODR8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA; pprdig=QtDwbJnM3e1gW52GsmpUOppHF2oNFRAE3BC5Jufvy5Z_9Lm0XYibiBqnoijSm0rl8LlthBskAJvgE2_I84muAZkdTjqSjpFTAOOrveJzdL3JNtKzHXHI-Mah0XqBCiWdXK6US082Sn5PtAW3UJQW5BXKdX9TxaqupHBPkKaozSE; ppinfo=e44814aa6e; passport=5|1627142284|1628351884|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIyODR8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA|31b08c800d|QtDwbJnM3e1gW52GsmpUOppHF2oNFRAE3BC5Jufvy5Z_9Lm0XYibiBqnoijSm0rl8LlthBskAJvgE2_I84muAZkdTjqSjpFTAOOrveJzdL3JNtKzHXHI-Mah0XqBCiWdXK6US082Sn5PtAW3UJQW5BXKdX9TxaqupHBPkKaozSE; sgid=24-53059563-AWD8OIxHvv7Fwpuf3ApgNec; ppmdig=16271422850000004a13b58c8e9e752018d91f85d9d3a95b'
}


def save_page_to_file(page, name):
    page_file = open(f'/text/article_sogou/{name}', 'w')
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
        try:
            content = catch_content_from_url(url, headers)
            save_page_to_file(content, filename)
            print(f'filename: {filename} save success')
        except:
            print(f'处理错误 url: {url}, filename: {filename}')


if __name__ == '__main__':
    urls = load_all_url_from_file('/Users/bytedance/PycharmProjects/pachong/text/sogou.txt')
    try:
        thread_01 = Thread(target=handle_page_from_url)
        thread_02 = Thread(target=handle_page_from_url)
        thread_03 = Thread(target=handle_page_from_url)
        thread_04 = Thread(target=handle_page_from_url)
        thread_05 = Thread(target=handle_page_from_url)
        thread_06 = Thread(target=handle_page_from_url)
        thread_07 = Thread(target=handle_page_from_url)
        thread_08 = Thread(target=handle_page_from_url)
        thread_09 = Thread(target=handle_page_from_url)
        thread_10 = Thread(target=handle_page_from_url)
        thread_11 = Thread(target=handle_page_from_url)
        thread_12 = Thread(target=handle_page_from_url)
        thread_01.start()
        thread_02.start()
        thread_03.start()
        thread_04.start()
        thread_05.start()
        thread_06.start()
        thread_07.start()
        thread_08.start()
        thread_09.start()
        thread_10.start()
        thread_11.start()
        thread_12.start()
    except:
        print("Error: 无法启动线程")
