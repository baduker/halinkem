#!/usr/bin/python3

import time
import os
import sys
import requests


from bs4 import BeautifulSoup as bs


DEFAULT_DIR = "my_halinki"
COMICS_DIR = os.path.join(os.getcwd(), DEFAULT_DIR)
BASE_URL = "http://www.pani-halinka.pl/main/"


LOGO = """
                                            ,
██╗  ██╗ █████╗ ██╗     ██╗███╗   ██╗██╗  ██╗███████╗███╗   ███╗
██║  ██║██╔══██╗██║     ██║████╗  ██║██║ ██╔╝██╔════╝████╗ ████║
███████║███████║██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██╔████╔██║
██╔══██║██╔══██║██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║
██║  ██║██║  ██║███████╗██║██║ ╚████║██║  ██╗███████╗██║ ╚═╝ ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ all!                                                                          
a comic scraper for tajo by baduker | v. 0.3 | github.com/baduker/halinkem
"""


def print_progress(iteration, total, prefix='', suffix='',
                   decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals
                                  in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' %
                     (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def get_image_comic_url(response):
    urls = []
    soup = bs(response.text, 'html.parser')
    for div in soup.find_all('div', id="comic_image"):
        for a in div.find_all('a'):
            for img in a.find_all('img', src=True):
                urls.append(img['src'])
    return urls


def get_main_urls():
    return [BASE_URL+str(i)+"/" for i in range(1, 32)]


def get_all_comic_src_urls(main_urls):
    counter = 0
    all_src_urls = []
    for page in range(len(main_urls)):
        print_progress(counter, len(
            main_urls), prefix='Finding Halinki:',
            suffix='Compelted!', bar_length=18)
        response = requests.get(main_urls[page])
        all_src_urls.append(get_image_comic_url(response))
        counter += 1
    return all_src_urls


def flat_list_of_all_src_urls(nested_array):
    return [src_url for src_url_sublist
            in nested_array for src_url
            in src_url_sublist]


def download_engine(url):
    file_name = url.split('/')[-1]
    with open(os.path.join(COMICS_DIR, file_name), "wb") as file:
        response = requests.get(url)
        file.write(response.content)


def halink_em_all(list_of_urls):
    counter = 0
    for src_url in list_of_urls:
        print_progress(counter, len(
            list_of_urls), prefix='Downloading Halinki:',
            suffix='Completed!', bar_length=18)
        download_engine(src_url)
        counter += 1


def main():

    print(LOGO)
    start = time.time()

    main_urls = get_main_urls()

    all_comic_src_urls = get_all_comic_src_urls(main_urls)

    flat_list = flat_list_of_all_src_urls(all_comic_src_urls)

    print("\nDone! All Halinki found.")

    os.makedirs(DEFAULT_DIR, exist_ok=True)

    halink_em_all(flat_list)

    end = time.time()
    print("\nFinished! {} Halinki downloaded in {:.2f} seconds.".format(
        len(flat_list), end - start))


if __name__ == '__main__':
    main()
