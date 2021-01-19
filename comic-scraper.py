import os
import shutil
import time
import sys
import numpy as np
import requests
import shared as sh

_try = False
true = True
false = False
recursion = 500

sys.setrecursionlimit(10000)
d = 0


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
    print("Chapter: " + str(chapter))


def get_page(comic_path, page, chapter):
    c = len(comic_path.split('/'))
    if c < 7:
        print("Fetching New Chapter... Please Wait1" + '\n')
        get_chapter(comic_path, chapter + 1)
    comic_path += '/' + str(page) + '.jpg'
    download_page(chapter, page, comic_path)


def download_page(chapter, page, comic_path):
    global d
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    d += 1
    if d % 50 == 0:
        delay = np.random.random(1000)
        if d>999:
            d = 0
        delay = delay[d]*1000
        print("Delay for ", delay, " ms")
        print('\n')

    response = requests.get(comic_path, stream=true, headers=headers)
    print(response.status_code)
    if response.status_code == 404:
        if page != 1:
            comic_path = comic_path.split('/')[:-2]
            comic_path = '/'.join(comic_path)
            print("Retrying... Please Wait!" + '\n')
            get_page(comic_path, page, chapter)
        else:
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


get_manga_name("hajime-no-ippo", chapter=588)
