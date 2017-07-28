import os
import subprocess
import sys

import xvfbwrapper


def take_screenshots(igv_script, preferences_file, screensize):
    width, height = screensize.split(',')
    with xvfbwrapper.Xvfb(width=width, height=height) as xvfb:
        exit_code = subprocess.call(['igv', '-o', preferences_file, '--batch', igv_script], env=os.environ.copy())
    sys.exit(exit_code)


if __name__ == '__main__':
    take_screenshots(sys.argv[1], sys.argv[2], sys.argv[3])

