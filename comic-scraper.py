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
    delay_exec()

def get_chapter(comic_path, chapter):
    # check if folder is available
    # else
    delay_exec()
    comic_path += '/' + str(chapter)
    print('\nFetching new Chapter!\nChapter: ', str(chapter), '\n')
    get_page(comic_path, 1, chapter)
    print(comic_path, chapter)

def get_page(comic_path, page, chapter):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    
    chap = sh.chapter_directory(chapter)
    filename = os.path.join(chap, str(page) + '.jpg')
    print(filename)
    if os.path.exists(filename):
       print('\n Page exists... Retriveing next page...!\n')
    else:
        c = len(comic_path.split('/'))
        if c < 7:
            print('\nFetching New Chapter... Please Wait1' + '\n')
            get_chapter(comic_path, chapter + 1)
        comic_path += '/' + str(page) + '.jpg'
        delay_exec()
        response = requests.get(comic_path, stream=true, headers=headers)
        print('\nresponse stautus code: ',response.status_code,'\n')
        
        if response.status_code == 404:
            comic_path = '.'.join(comic_path.split('.')[:-1])
            response_post_ext = check_extensions(comic_path, headers, filename)
            if response_post_ext != 404:
                comic_path = comic_path.split('/')[:-1]
                comic_path = '/'.join(comic_path)
                get_page(comic_path, page, chapter)
            elif response_post_ext == 404 and page != 1:
                comic_path = comic_path.split('/')[:-2]
                comic_path = '/'.join(comic_path)
                get_chapter(comic_path, chapter+1)
            else:
                print('\nCHAPTER NOT RELEASED YET...!\n')
                exit()
        else:
            download_page(response, filename)
            comic_path = comic_path.split('/')[:-1]
            comic_path = '/'.join(comic_path)
    get_page(comic_path, page + 1, chapter)

def download_page(response, filename):
    delay_exec()
    response.raw.decode_content = true
    with open(filename, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    print('\nDownload Successful!\n')
    
def delay_exec():
    global d
    d += 1
    if d % 50 == 0:
        delay = np.random.random(1000)
        if d>999:
            d = 0
        delay = delay[d]*10
        time.sleep(delay)
        print("Delay for ", delay, " s")
        print('\n')

def check_extensions(comic_path, headers, filename):
    dummy = 0
    comic_path_png = comic_path+'.png'
    comic_path_jpg = comic_path+'.jpg'
    comic_path_d = ''
    while dummy < 2:
        if dummy % 2 == 0:
            comic_path_d = comic_path_png
        else:
            comic_path_d = comic_path_jpg
        dummy+=1
        delay_exec()
        response = requests.get(comic_path_d, stream=true, headers=headers)
        if response.status_code != 404:
            comic_path = comic_path_d
            print('\ncomic path after extension change: ', comic_path, '\n')
            download_page(response, filename)
            break
        print('\nresponse status code after extension change: ',response.status_code,'\n')
        return response.status_code
    
get_manga_name('jujutsu-kaisen', chapter=88)
