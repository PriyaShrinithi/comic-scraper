import os
from bs4 import BeautifulSoup
import re
import urllib.request
import requests
import shutil

true = True
false = False

pages = set()
page = set()
chapters = set()
comic_path = 'https://www.mangareader.net/shingeki-no-kyojin/'
#upon updates receive url or last part of url from user

drive =  'D:'
#upon updates, receive the drive from user
comic_directory = 'Comics'
manga_directory = comic_path.split('/')[-2]
parent_path = os.path.join(drive, comic_directory, manga_directory)

if not os.path.exists(parent_path):
    os.mkdir(parent_path)
    
def get_page(ch_no):
    if ch_no not in chapters:
        chapters.add(ch_no)
        comic = urllib.request.urlopen(comic_path+str(ch_no))
        soup = BeautifulSoup(comic, 'html.parser')
        pg_links = soup.find(id='main').find('script')
        pg_links = str(pg_links)
        pages = pg_links.split('[')
        pages = pages[2].split('=')
        pages = pages[0].split(']')
        pages = pages[0]
        pages = pages.split('},')
        ch_path = os.path.join(parent_path, str(ch_no))
        pg_no = 1
        for pg in pages:
            if '}' not in pg:
                pg = pg+'}'
            pg = eval(pg)
            pg = pg['u']
            pg = pg.replace('\\', '') # to clean the link url
            if pg not in page:
                page.add(pg)
                page_path = 'https:'+pg
                download_page(page_path, pg_no, ch_path)
            pg_no+=1
        get_page(ch_no+1)
        

def download_page(page_path, pg_no, ch_path):
    if not os.path.exists(ch_path):
        os.mkdir(ch_path)
    filename = os.path.join(ch_path, str(pg_no)+'.jpg')
    if not os.path.exists(filename):
        req = requests.get(page_path, stream = true)
        req.raw.decode_content = true
        if req.status_code == 200:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(req.raw, f)
            print('Download Successful!')
        else:
            print(req.status_code)
            print('Downloading Again...')
            download_page(page_path, pg_no, ch_path)
    else:
        print('File Exists')
    
get_page(27)
print('Done')
# DND, except to alter if value and clean the final pg
