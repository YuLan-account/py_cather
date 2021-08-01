import ahocorasick


def load_content_from_file(file_dir):
    file = open(file_dir, 'r')
    content = file.read()
    return content


def test():
    tree = ahocorasick.AhoCorasick("吃饭", "睡觉", "玩耍", "上班")  # 构建ac自动机
    res = tree.search("我喜欢吃饭睡觉玩耍上班")
    print(type(res))
    print(res.__contains__("吃饭"))
    print(tree.search("我喜欢吃饭睡觉玩耍上班"))  # 检索


def main():
    content = load_content_from_file('../text/article_baidu/baidu_page_1.txt')
    print(content)


if __name__ == '__main__':
    main()
