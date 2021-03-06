import requests
from lxml import etree
import re
import random
import json
from bs4 import BeautifulSoup
from urllib import parse
from threading import Thread, Lock

file_prefix = 'sogou_page_'
file_suffix = '.txt'
file_name_index = 0

page_index = 1

UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"

search_key = "农业视频会议 县"

page_index_lock = Lock()
filename_index_lock = Lock()

weixinIndexVisited = 1
ppinf = '5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA;'
pprdig = 'QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo;'
ppinfo = 'e7428eb679;'
passport = '5|1627142393|1628351993|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxNDIzOTN8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA|8bc25f0a78|QRauHV08EUupRWvyUBIDGH1M0mEEqTt2ZrCUC29C4Wi0D_zhhq5_RBGgxqjKYs5w8NzgR4EVZeeVo68ScDvSU5BaT1CKC7PJXpKS3EPjghTvw2SbZw_PVDWBz8-ohfEgeD2_VSwaua55QSy-yFuJLmdiCq1LXy-XP71gzc4W5Fo;'
sgid = '24-53059563-AWD8OPncjs8DsDmrMh4bV4o;'
ppmdig = '1627181377000000ef90d3ac2b840a9abcf3e8d04545a3ee'


headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "weixin.sogou.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent,
}


def get_cookie(response1, uigs_para, UserAgent):
    SetCookie = response1.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0],
        "weixinIndexVisited": weixinIndexVisited,
        "ppinf": ppinf,
        "pprdig": pprdig,
        "ppinfo": ppinfo,
        "passport": passport,
        "sgid": sgid,
        "ppmdig": ppmdig
    }

    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response2 = requests.get(url, headers=headers)
    SetCookie = response2.headers['Set-Cookie']
    cookie_params['SUID'] = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'],
                                                                  cookie_params['IPLOC'],
                                                                  cookie_params['SUID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent
    }
    response3 = requests.get(url, headers=headers)
    SetCookie = response3.headers['Set-Cookie']
    cookie_params['JSESSIONID'] = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]

    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'],
                                                       cookie_params['SUID']),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response4 = requests.get(url, headers=headers, params=uigs_para)
    SetCookie = response4.headers['Set-Cookie']
    cookie_params['SUV'] = re.findall('SUV=(.*?);', SetCookie, re.S)[0]

    return cookie_params


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def get_uigs_para(response):
    uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
    if 'passportUserId ? "1" : "0"' in uigs_para:
        uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
    uigs_para = json.loads(uigs_para)
    exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
    uigs_para['right'] = 'right0_0'
    uigs_para['exp_id'] = exp_id[:-1]
    return uigs_para


def handle_page(list_url, UserAgent):
    response1 = requests.get(list_url, headers=headers1)
    html = etree.HTML(response1.text)
    urls = ['https://weixin.sogou.com' + i for i in html.xpath('//div[@class="img-box"]/a/@href')]

    uigs_para = get_uigs_para(response1)
    params = get_cookie(response1, uigs_para, UserAgent)
    for url in urls:
        url = get_k_h(url)
        headers3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "ABTEST={}; "
                      "SNUID={}; "
                      "IPLOC={}; "
                      "SUID={}; "
                      "JSESSIONID={}; "
                      "SUV={} ".format(params['ABTEST'],
                                         params['SNUID'],
                                         params['IPLOC'],
                                         params['SUID'],
                                         params['JSESSIONID'],
                                         params['SUV']),
            "Host": "weixin.sogou.com",
            "Referer": list_url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent
        }
        response3 = requests.get(url, headers=headers3)

        fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
        itemurl = ''
        for i in fragments:
            itemurl += i

        # 文章url拿正文
        headers4 = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": UserAgent
        }
        print(f'thread name: {Thread.name} url: {itemurl}')
        response4 = requests.get(itemurl, headers=headers4)
        page = response4.content.decode()
        soup = BeautifulSoup(page, 'html.parser')
        soup.script.decompose()
        contents = soup.find_all('p')
        all_content = ""
        for content in contents:
            all_content += content.get_text() + '\n'
        save_page_to_file(all_content, )


def save_page_to_file(page, name):
    page_file = open(f'/Users/bytedance/PycharmProjects/pachong/text/article_sogou/{name}', 'w')
    page_file.write(page)
    page_file.flush()


def task():
    global search_key, headers1
    global page_index
    global file_name_index
    global UserAgent
    while page_index < 100:
        with page_index_lock:
            page = page_index
            page_index += 1
        try:
            print(f'cur thread name: {Thread.name}, page: {page}')
            list_url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&_sug_=n&_sug_type_=&page={}'.format(
                parse.quote(search_key), page)
            response1 = requests.get(list_url, headers=headers1)
            html = etree.HTML(response1.text)
            urls = ['https://weixin.sogou.com' + i for i in html.xpath('//div[@class="img-box"]/a/@href')]

            print(urls)

            uigs_para = get_uigs_para(response1)
            params = get_cookie(response1, uigs_para, UserAgent)

            for url in urls:
                url = get_k_h(url)
                headers3 = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Connection": "keep-alive",
                    "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                                     params['SNUID'],
                                                                                                     params['IPLOC'],
                                                                                                     params['SUID'],
                                                                                                     params['JSESSIONID'],
                                                                                                     params['SUV']),
                    "Host": "weixin.sogou.com",
                    "Referer": list_url,
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": UserAgent
                }
                response3 = requests.get(url, headers=headers3)

                fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
                itemurl = ''
                for i in fragments:
                    itemurl += i

                # 文章url拿正文
                headers4 = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "cache-control": "max-age=0",
                    "user-agent": UserAgent
                }
                print(f'thread name: {Thread.name} url: {itemurl}')
                response4 = requests.get(itemurl, headers=headers4)
                page = response4.content.decode()
                soup = BeautifulSoup(page, 'html.parser')
                soup.script.decompose()
                contents = soup.find_all('p')
                all_content = ""
                for content in contents:
                    all_content += content.get_text() + '\n'
                with filename_index_lock:
                    filename = file_prefix + f'{file_name_index}' + file_suffix
                    file_name_index += 1

                save_page_to_file(all_content, filename)

        except:
            print('unknown error')


if __name__ == "__main__":
    thread_01 = Thread(target=task)
    thread_01.start()

    thread_02 = Thread(target=task)
    thread_02.start()

    thread_03 = Thread(target=task)
    thread_03.start()

    thread_04 = Thread(target=task)
    thread_04.start()

    thread_05 = Thread(target=task)
    thread_05.start()

    thread_06 = Thread(target=task)
    thread_06.start()



