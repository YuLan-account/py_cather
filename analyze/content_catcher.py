import requests
from bs4 import BeautifulSoup
import ssl
import re

headers = {
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept-Language": 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Cache-Control': 'max-age=0',
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Cookie': 'ABTEST=0|1627100203|v1; IPLOC=CN4403; SUID=7E1388774842910A0000000060FB942B; weixinIndexVisited=1; SUV=00F9E6617788137E60FB942C9C96B467; JSESSIONID=aaaaLEjYZS1N49gRmf_Ox; ppinf=5|1627111952|1628321552|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxMTE5NTJ8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA; pprdig=K_xGt7sZgF2lWWaIDTdLN20Ykm09-MJA1YduF4JnXG2_f0LAe5QX9d4hU2jeEHdXxSjyBlSoW9OJle31VIQ6olHVardGGOdxFLOacBVv7okOd-rJjv3H0EDD9ErYBQ1xsy-E2UIapcstVeU_KHJuwrS-pEXz4w7qbHf4ppZBs6w; ppinfo=bf44ca98e1; passport=5|1627111952|1628321552|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQkUlQkQlRTglOTMlOUR8Y3J0OjEwOjE2MjcxMTE5NTJ8cmVmbmljazoxODolRTclQkUlQkQlRTglOTMlOUR8dXNlcmlkOjQ0Om85dDJsdUg4c0NjOWVHWnZmeVBaMHRwdmkxT2NAd2VpeGluLnNvaHUuY29tfA|4ef460ac74|K_xGt7sZgF2lWWaIDTdLN20Ykm09-MJA1YduF4JnXG2_f0LAe5QX9d4hU2jeEHdXxSjyBlSoW9OJle31VIQ6olHVardGGOdxFLOacBVv7okOd-rJjv3H0EDD9ErYBQ1xsy-E2UIapcstVeU_KHJuwrS-pEXz4w7qbHf4ppZBs6w; sgid=24-53059563-AWD7whALrej4YgptPn3UXMs; ppmdig=1627135406000000da4e20218bad20ef3b6957dbc9889daa; PHPSESSID=hvpptqr5sritvs68b7oplt8m10; seccodeErrorCount=1|Sat, 24 Jul 2021 14:08:36 GMT; SNUID=5634A0502722EFF6DBE053582832A34B; seccodeRight=success; successCount=1|Sat, 24 Jul 2021 14:08:41 GMT'
}


def get_snuid():
    # 此url为在搜狗网站找到的可以持续生成snuid的链接，此url只是给个例子，搜狗网站里这么多网页，多翻翻会有惊喜的
    # 做爬虫要有耐心，去找规律。
    url = 'https://www.sogou.com'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    rst = requests.get(url=url, headers=headers)
    print(rst.headers)
    pattern = r'SNUID=(.*?);'
    snuid = re.findall(pattern, str(rst.headers))[0]
    return snuid


def catch_content_from_url(url, headers):
    ssl._create_default_https_context = ssl._create_unverified_context
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    contents = soup.find_all('p')
    all_content = ""
    for content in contents:
        all_content += (content.get_text())

    print(f"all content: {all_content}")
    return all_content


def catch_content_from_sogou_url(url, headers):
    page = requests.get(url=url, headers=headers)
    js_text = page.text
    real_url = ''
    parts = re.findall(r'\+\=\ \'.+', js_text)

    for i in parts:
        real_url += i[4:-3]
    real_url.replace("@", "")
    print(f'real_url: {real_url}')
    return catch_content_from_url(real_url, headers)


if __name__ == '__main__':
    url = 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS__DpAEUXSDTvZ6RH6OrP1Ms8jvuJSs1cFqXa8Fplpd94M1dX2D6r_yMT-KuW9btQFeNXDH2j6jaP2qr6BhjW4ONvkMtuBKdOmNkdq593POO4moY6aql05k95ZjvftXvGu0cCoQGyKvEj1u6muIyaWPfGg0R9BFrBQT1d4EgrvWDQUsqvMZFE2GA_dtc5LcuyQExRFDMD2YPd9aH0XuaSBjzAjcIGepUqA..&type=2&query=%E5%86%9C%E4%B8%9A%E8%A7%86%E9%A2%91%E4%BC%9A%E8%AE%AE %E5%8E%BF&token=4B666B2776148F70070DC0D82882A9220886845460FCD706'
    # real_url = 'http://mp.weixin.qq.com/s?src=11&timestamp=1627182855&ver=3211&signature=pfWlcPI-iDmQ6GHSMI1bRyzbTSZny*kPhuDyyds16doS9H2LFcxRa*ELXRr18Al72AZ1yPFexalXCnSA7FiSZDKGyMJc5SwEXMz8DdoUEnRVWaFnWXxzjUg0xrN26gP-&new=1'
    sogou_content = catch_content_from_sogou_url(url, headers)
    print(sogou_content)