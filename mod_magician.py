import re
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from mods import Mods, CharReqs


def parse_args():
    parser = ArgumentParser(
        description='Optimise your mods',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('modsin', type=str,
                        help="path to read extracted mods from")
    parser.add_argument('charsin', type=str,
                        help="path to read character requirements from")
    parser.add_argument('modsout', type=str,
                        help="path to store mods and suggested new toons in")
    parser.add_argument('-d', '--delimeter', type=str, default=',',
                        help="delimeter to separate outputs by")
    parsed = parser.parse_args()
    return parsed


def load_chars_from_file(charsin, delimeter):
    chars = []
    with open(charsin) as inf:
        for line in inf:
            if not line.startswith('#'):
                entries = line.lower().strip().split(delimeter)
                chars.append(CharReqs(
                    entries[0],
                    [x for x in entries[3:6] if x is not ''],
                    [x for x in entries[6:9] if x is not ''],
                    [x for x in entries[9:12] if x is not ''],
                    entries[1],
                    entries[2]
                ))
    return chars


def main():
    opts = parse_args()
    mods = Mods()
    mods.load_mods_from_file(opts.modsin, opts.delimeter)
    chars = load_chars_from_file(opts.charsin, opts.delimeter)
    for char in chars:
        mods.assign_mods(char)
    mods.write_mods_to_file(opts.modsout, opts.delimeter)


if __name__ == '__main__':
    main()
