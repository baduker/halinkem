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
 __ __   ____  _      ____  ____   __  _ __    ___  ___ ___       ____  _      _      __ 
|  |  | /    || |    |    ||    \ |  |/ ]  |  /  _]|   |   |     /    || |    | |    |  |
|  |  ||  o  || |     |  | |  _  ||  ' /|_ | /  [_ | _   _ |    |  o  || |    | |    |  |
|  _  ||     || |___  |  | |  |  ||    \  \||    _]|  \_/  |    |     || |___ | |___ |__|
|  |  ||  _  ||     | |  | |  |  ||     \   |   [_ |   |   |    |  _  ||     ||     | __ 
|  |  ||  |  ||     | |  | |  |  ||  .  |   |     ||   |   |    |  |  ||     ||     ||  |
|__|__||__|__||_____||____||__|__||__|\_|   |_____||___|___|    |__|__||_____||_____||__|
                                                                                         
  a comic scraper for tajo by baduker | version: 0.1 | repo: github.com/baduker/halinkem
"""


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

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
  return [BASE_URL+str(i)+"/" for i in range(1,32)]


def flat_list_of_all_src_urls(nested_array):
  return [src_url for src_url_sublist in nested_array for src_url in src_url_sublist]


def download_engine(url):
  file_name = url.split('/')[-1]
  with open(os.path.join(COMICS_DIR, file_name), "wb") as file:
    response = requests.get(url)
    file.write(response.content)


def main():

  print(LOGO)
  start = time.time()

  main_urls = get_main_urls()


  counter = 0
  all_src_urls = []
  for page in range(len(main_urls)):
    print_progress(counter, len(main_urls), prefix = 'Finding Halinki', suffix = ' Compelte', bar_length = 18)
    response = requests.get(main_urls[page])
    all_src_urls.append(get_image_comic_url(response))
    counter += 1

  flat_list = flat_list_of_all_src_urls(all_src_urls)

  print("\nDone!")

  os.makedirs(DEFAULT_DIR, exist_ok = True)

  counter = 0
  for i in flat_list:
    print_progress(counter, len(flat_list), prefix = 'Downloading Halinki', suffix = 'Complete', bar_length = 18)
    download_engine(i)
    counter += 1

  end = time.time()
  print("\n{} Halinki downloaded in {:.2f} seconds".format(len(flat_list), end - start))


if __name__ == '__main__':
  main()