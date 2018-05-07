import re
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from bs4 import BeautifulSoup
import requests


def parse_args():
    parser = ArgumentParser(
        description='Extract mods from swgoh.gg',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('username', type=str,
                        help="swgoh.gg username")
    parser.add_argument('outfile', type=str,
                        help="path to store extracted mods in")
    parsed = parser.parse_args()
    return parsed


def get_num_pages(username):
    url='https://swgoh.gg/u/{}/mods/'.format(username)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for line in soup.find_all('li'):
        if line.string:
            mat = re.search(r'Page 1 of (\d+)', line.string)
            if line.string:
                return int(mat.group(1))
    # log that could not parse mod page
    print("Could not parse the page properly")
    sys.exit(1)


def get_mods(pages, username):
    for page in range(1, 2): #pages+1):
        print("Parsing page {} of {}".format(page, pages))
        url='https://swgoh.gg/u/{}/mods/?page={}'.format(username, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all("div", {'class': "collection-mod"}):
            current_toon = item.find("div", {'class': "char-portrait"}).get('title')
            print("{}".format(current_toon))
        time.sleep(0.5)


def main():
    opts = parse_args()
    num_pages = get_num_pages(opts.username)
    print("Num pages {}".format(num_pages))
    mods = get_mods(num_pages, opts.username)


if __name__ == '__main__':
    main()
