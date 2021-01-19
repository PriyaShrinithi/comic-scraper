import time
import os
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import json
import shared as sh

true = True
false = False

global soup
headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}

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
    print("Chapter: "+chapter)


def get_page(comic_path, page, chapter):
    comic_path += '/' + str(page) + '.jpg'
    print(comic_path)
    download_page(chapter, page, comic_path)


def download_page(chapter, page, comic_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    response = requests.get(comic_path, stream=true)
    print(response.status_code)
    if response.status_code == 404:
        if page != 1:
            comic_path = comic_path.split('/')[:-2]
            comic_path = '/'.join(comic_path)
            get_chapter(comic_path, chapter + 1)
        else:
        # delete last made directory and exit
            exit()
    else:
        chap = sh.chapter_directory(chapter)
        filename = os.path.join(chap, str(page)+'.jpg')
        print(filename)
        if os.path.exists(filename):
            get_page(comic_path, page+1, chapter)
        else:
            response.raw.decode_content = true
            with open(filename, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print('Download Successful!')
        comic_path = comic_path.split('/')[:-1]
        comic_path = '/'.join(comic_path)
        get_page(comic_path, page + 1, chapter)
    '''


def download_page(page_path, pg_no, ch_path):
    print(ch_path)
    tic_ = time.time()
    if not os.path.exists(ch_path):
        os.mkdir(ch_path)
    filename = os.path.join(ch_path, str(pg_no) + '.jpg')
    if not os.path.exists(filename):
        req = requests.get(page_path, stream=true)
        req.raw.decode_content = true
        if req.status_code == 200:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(req.raw, f)
            print('Download Successful!')
        else:
            print(req.status_code)
            print('ch: ' + ch_path + ' pg: ' + str(pg_no) + ' Downloading Again...')
            download_page(page_path, pg_no, ch_path)
    else:
        print('File Exists')
    toc_ = time.time()
    print('download page: ', (toc_ - tic_) * 1000)'''


get_manga_name("one-piece", chapter=1001)
