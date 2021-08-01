import os

def clean_file():
    base_dir = '/Users/bytedance/PycharmProjects/pachong/result/sogou/pages1/'
    base_file_name = 'sogou_page_'
    for index in range(0, 2000):
        file_dir = base_dir + base_file_name + "" + str(index) + ".txt"
        if os.path.exists(file_dir):
            file = open(file_dir, 'r')
            contents = file.readlines()
            all_content = ""
            for content in contents:
                all_content += content

            if len(all_content) < 30:
                os.remove(file_dir)
                print(f'移除文件 {file_dir}')

def rename_file():
    base_dir = '/Users/bytedance/PycharmProjects/pachong/result/sogou/pages1/'
    base_file_name = 'sogou_page_'
    file_idx = 1
    for index in range(0, 2000):
        file_dir = base_dir + base_file_name + "" + str(index) + ".txt"
        if os.path.exists(file_dir):
            new_filename = base_dir + base_file_name + str(file_idx) + ".txt"
            os.rename(file_dir, new_filename)
            file_idx += 1
            print(f'重命名：{file_dir} -> {new_filename}')


if __name__ == '__main__':
    rename_file()
