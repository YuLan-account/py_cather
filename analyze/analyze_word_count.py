import operator
import sys

sys.path.append("../")
import requests
from bs4 import BeautifulSoup
import jieba

# 定义要删除的标点符号
add_punc = '，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'

# 定义要去除的停词
stop = [line.strip() for line in open('../res/cn.stopwords.txt').readlines()]

if __name__ == '__main__':
    # url = 'https://baijiahao.baidu.com/s?id=1701614910969973169&wfr=spider&for=pc'
    url = 'https://www.163.com/dy/article/GEP2JI6C0550NTPH.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    contents = soup.find_all('p')
    all_content = ""
    for content in contents:
        all_content += content.get_text() + '\n'
    print(all_content)
    # jieba_content = " ".join(jieba.cut(all_content))
    # content_list = jieba_content.split(" ")
    #
    # content_list2 = []
    # for content in content_list:
    #     content_list2.append(content)
    #     if content in add_punc or content in stop:
    #         content_list2.remove(content)
    # word_map = {k: content_list2.count(k) for k in content_list2}
    #
    # sorted_tuples = sorted(word_map.items(), key=operator.itemgetter(1), reverse=True)
    # # 取前10多
    # sorted_dict = {k: v for k, v in sorted_tuples[0:10]}
    # for key, value in sorted_dict.items():
    #     print(key, "  的出现次数 ： ", value, " 次")