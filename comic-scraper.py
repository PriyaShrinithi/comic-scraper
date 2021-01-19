import os
import shutil
import time

import numpy as np
import requests
import shared as sh

true = True
false = False

global soup


def get_manga_name(manga, chapter):
    comic_path = 'https://img.mghubcdn.com/file/imghub'
    comic_path += '/' + manga
    print(comic_path)
    sh.main_directory(comic_path)
    get_chapter(comic_path, chapter)


def get_chapter(comic_path, chapter):
    # check if folder is available
    # else
    comic_path += '/' + str(chapter)
    get_page(comic_path, 1, chapter)
    print(comic_path, chapter)
    print("Chapter: " + chapter)


def get_page(comic_path, page, chapter):
    comic_path += '/' + str(page) + '.jpg'
    print(comic_path)
    download_page(chapter, page, comic_path)


def download_page(chapter, page, comic_path):
    global d
    d = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    response = requests.get(comic_path, stream=true)
    print(response.status_code)
    if response.status_code == 404:
        if page != 1:
            comic_path = comic_path.split('/')[:-3]
            comic_path = '/'.join(comic_path)
            get_chapter(comic_path, chapter + 1)
        else:
            # delete last made directory and exit
            exit()
    else:
        chap = sh.chapter_directory(chapter)
        filename = os.path.join(chap, str(page) + '.jpg')
        print(filename)
        if os.path.exists(filename):
            get_page(comic_path, page + 1, chapter)
        else:
            response.raw.decode_content = true
            with open(filename, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print('Download Successful!')
        comic_path = comic_path.split('/')[:-1]
        comic_path = '/'.join(comic_path)
        get_page(comic_path, page + 1, chapter)
        d += 1
        if d % 50 == 0:
            delay = np.random.random(1000000)
            time.sleep(delay)


get_manga_name("hajime-no-ippo", chapter=1)
