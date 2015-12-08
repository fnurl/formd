# coding=utf8
"""Command line script for running formd.

Author: Seth Brown
Date: 30 Mar 2013
"""

import sys
import argparse
import formd


def main():
    """Command line options."""
    description = 'formd: A (for)matting (M)ark(d)own tool.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('-r', '--ref', help='convert text to referenced Markdown',
                   action='store_true', default=False)
    p.add_argument('-i', '--inline', help='convert text to inline Markdown',
                   action='store_true', default=False)
    p.add_argument('-f', '--flip', help='convert to opposite style Markdown',
                   action='store_true', default=True)
    args = p.parse_args()
    md = sys.stdin.read()
    f = formd.ForMd(md)
    if (args.inline):
        [sys.stdout.write(t) for t in f.inline_md()]
    elif (args.ref):
        [sys.stdout.write(t) for t in f.ref_md()]
    elif (args.flip):
        [sys.stdout.write(t) for t in f.flip()]

if __name__ == '__main__':
    main()
