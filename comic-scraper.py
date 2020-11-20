import time
import os
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import tqdm

tic = time.time()
true = True
false = False
pages = set()
page = set()
chapters = set()
comic_path = 'https://www.mangareader.net/acmagame'

comic = urllib.request.urlopen(comic_path)
soup = BeautifulSoup(comic, 'html.parser')
#upon updates receive url or last part of url from user

drive =  'D:'
#upon updates, receive the drive from user
comic_directory = 'Comics'
manga_directory = soup.find(class_='d40').text.split(' Manga')[0]
parent_directory = os.path.join(drive, comic_directory, manga_directory)
print(manga_directory)

if not os.path.exists(parent_directory):
    try:
        os.mkdir(parent_directory)
    except:
        manga_directory = ' '.join(manga_directory.split(':'))    
        parent_directory = os.path.join(drive, comic_directory, manga_directory)
        if not os.path.exists(parent_directory):
            os.mkdir(parent_directory)
    
chap = list()

def get_chapters():
    tic_ = time.time()
    #comic = urllib.request.urlopen(comic_path)
    ch_links = soup.find(class_='d48').findChildren('a')
    for link in ch_links:
        if 'href' in link.attrs:
            if link['href'] not in chap:
                new_chapter = link.attrs['href'].split('/')[-1]
                chap.append(new_chapter)
    toc_ = time.time()
    print('get chapters: ',(toc_ - tic_)*1000, ' ms')

def get_chapter(ch_no):
    tic_ = time.time()
    try:
        ch = chap[ch_no - 1]
    except:
        print('Done!')
        exit()
        
    if str(ch) in chap:
        get_page(ch, ch_no)
        
def get_page(ch, chap_index):    
    if ch not in chapters:
        chapters.add(ch)
        comic = urllib.request.urlopen(comic_path+'/'+str(ch))
        soup = BeautifulSoup(comic, 'html.parser')
        pg_links = soup.find(id='main').find('script')
        pg_links = str(pg_links)
        pages = pg_links.split('[')
        try:
            pages = pages[2].split('=')
        except:
            print('Checking for continuity errors...')
            get_chapter(chap_index+1)
        pages = pages[0].split(']')
        pages = pages[0]
        pages = pages.split('},')
        ch_path = os.path.join(parent_directory, str(ch))
        pg_no = 1
        
        for pg in pages:
            if '}' not in pg:
                pg = pg+'}'
                pg = eval(pg)
                pg = pg['u']
                pg = pg.replace('\\', '') # to clean the link url
                if pg not in page:
                    pg = 'https:'+pg
                    download_page(pg, pg_no, ch_path)
                    page.add(pg)
            pg_no+=1
        get_chapter(chap_index+1)
    toc_ = time.time()
    print('get page: ', (toc_ - tic_)*1000, ' ms')
            
def download_page(page_path, pg_no, ch_path):
    print(ch_path)
    tic_ = time.time()
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
            print('ch: '+ch_path+' pg: '+str(pg_no)+' Downloading Again...')
            tqdm(download_page(page_path, pg_no, ch_path))
    else:
        print('File Exists')
    toc_ = time.time()
    print('download page: ',(toc_ - tic_)*1000)

#def get_page_url(pg_no):
    
get_chapters()
tqdm(get_chapter(1))
toc = time.time()
print('comic-scraper: ',(toc-tic)*1000, ' ms')
# DND, except chapter number and mangalink
