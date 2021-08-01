
def load_all_url_from_file(file_dir):
    file = open(file_dir, 'r')  # write append
    urls = file.readlines()
    res = []
    for url in urls:
        new_url = url.strip('\n')
        if new_url != "":
            res.append(new_url)
    return res


def save_page_to_file(dir, page, filename):
    page_file = open(f'{dir}/{filename}', 'w')
    page_file.write(page)
    page_file.flush()
