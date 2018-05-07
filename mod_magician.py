import re
import sys
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from mods import Mods


def parse_args():
    parser = ArgumentParser(
        description='Optimise your mods',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('infile', type=str,
                        help="path to read extracted mods from")
    parser.add_argument('outfile', type=str,
                        help="path to store mods and suggested new toons in")
    parser.add_argument('-d', '--delimeter', type=str, default=',',
                        help="delimeter to separate outputs by")
    parsed = parser.parse_args()
    return parsed


def main():
    opts = parse_args()
    mods = Mods()
    mods.load_mods_from_file(opts.infile, opts.delimeter)
    mods.write_mods_to_file(opts.outfile, opts.delimeter)
    for mod in mods.filter_mods(level=15, pips=5, modshape='arrow', primary='speed'):
        print(mod.to_xsv())


if __name__ == '__main__':
    main()
