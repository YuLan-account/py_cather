from pprint import pprint

from baiduspider import BaiduSpider


target_file = open('../result/baidu_link.txt', 'a')


def save_link_to_file(link_set):
    links = ''
    for link in link_set:
        links = links + link + '\n'
    print(links)
    target_file.write(links + '\n')
    target_file.flush()


if __name__ == '__main__':
    # 实例化BaiduSpider
    spider = BaiduSpider()

    # 搜索网页
    # for index in range(0, 45):
    #     print(f'第{index}次爬取搜索结果')
    index = 0
    while True:
        on = input()
        if on == 'f':
            print(f'第{index}次抓取搜索结果')
            res = spider.search_web(query='intitle: 农业视频会议 县', pn=int(index))
            pprint(res)
            res_arr = res['results']
            link_set = set([])
            for i in range(2, len(res_arr)):
                if res_arr[i]['title'] is not None:
                    title = res_arr[i]['title']
                    url = res_arr[i]['url']
                    link = title + "|" + url
                    link_set.add(link)
            save_link_to_file(link_set)

        print(f'完成第{index}次抓取，请输入f进行下一次抓取...')
        index += 1