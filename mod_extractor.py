import re
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from bs4 import BeautifulSoup
import requests
from mods import Mod, Mods, ModStat


def parse_args():
    parser = ArgumentParser(
        description='Extract mods from swgoh.gg',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('username', type=str,
                        help="swgoh.gg username")
    parser.add_argument('outfile', type=str,
                        help="path to store extracted mods in")
    parser.add_argument('-d', '--delimeter', type=str, default=',',
                        help="delimeter to separate outputs by")
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
    mods = Mods()
    for page in range(1, pages+1):
        print("Parsing page {} of {}".format(page, pages))
        url='https://swgoh.gg/u/{}/mods/?page={}'.format(username, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all("div", {'class': "collection-mod"}):
            current_toon = item.find("div", {'class': "char-portrait"}).get('title')
            pips = len(item.find_all("span", {'class': "statmod-pip"}))
            level = int(item.find("span", {'class': "statmod-level"}).string)
            moddesc = item.find("img", {'class': "statmod-img"}).get('alt').split()
            modset = " ".join(moddesc[2:-1])
            modshape = moddesc[-1]
            prim = item.find('div', {'class': "statmod-stats statmod-stats-1"})
            primstat = prim.find('span', {'class': "statmod-stat-label"}).string
            primvalue = prim.find('span', {'class': "statmod-stat-value"}).string.lstrip('+')
            if primvalue.endswith('%'):
                primstat += '%'
                primvalue = primvalue[:-1]
            primary = ModStat(primstat, primvalue)
            secondaries = []
            esses = item.find("div", {'class': "statmod-stats statmod-stats-2"})
            for secondary in esses.find_all("div", {'class': "statmod-stat"}):
                s_stat = secondary.find('span', {'class': "statmod-stat-label"}).string
                s_value = secondary.find('span', {'class': "statmod-stat-value"}).string.lstrip('+')
                if s_value.endswith('%'):
                    s_stat += "%"
                    s_value = s_value[:-1]
                secondaries.append(ModStat(s_stat, s_value))
            mod = Mod(current_toon, pips, level, modset, modshape, primary, secondaries)
            mods.add_mod(mod)
        time.sleep(0.5)
    return mods


def main():
    opts = parse_args()
    num_pages = get_num_pages(opts.username)
    print("Num pages {}".format(num_pages))
    mods = get_mods(num_pages, opts.username)
    mods.write_mods_to_file(opts.outfile, opts.delimeter)


if __name__ == '__main__':
    main()
