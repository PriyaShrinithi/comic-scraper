import bs4 as BeautifulSoup
import os


class shared:
    global drive
    # upon updates, receive the drive from user
    global comic_directory

def main_directory(link):
    global manga_directory
    global parent_directory
    drive = 'D:'
    comic_directory = 'Comics'

    soup = BeautifulSoup
    manga_directory = link.split('/')[-1].replace("-", " ").title()
    parent_directory = os.path.join(drive, comic_directory, manga_directory)
    print(parent_directory)

    if not os.path.exists(parent_directory):
        try:
            os.mkdir(parent_directory)
        except:
            manga_directory = ' '.join(manga_directory.split(':'))
            parent_directory = os.path.join(drive, comic_directory, manga_directory)
            if not os.path.exists(parent_directory):
                os.mkdir(parent_directory)
        parent_directory = os.path.join(drive, comic_directory, manga_directory)
        print(manga_directory)
        return None

def chapter_directory(chapter):
    chapter = str(chapter)
    chapter_dir = os.path.join(parent_directory, chapter)
    if os.path.exists(chapter_dir):
        pass
    else:
        os.mkdir(chapter_dir)
    return chapter_dir