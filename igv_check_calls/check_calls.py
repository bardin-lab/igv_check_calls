"""Goes through a list of images. The user can press 'n' or 'y',
which will cause True or False to be written in the output file as a column next to the filename.
Prerequisite is a functional opencv library (on OSX can be installed by brew install opencv), pyobjc (pip install pyobjc)
and opencv-python
"""

from collections import OrderedDict
import os
import click
import cv2
from AppKit import NSScreen

from .igv import IGV


class CheckImages(object):
    """Check a series of images, optionally see images in detail in IGV."""

    def __init__(self, files, control_igv, output_path='output.tsv'):
        self.files = OrderedDict()
        for file in files:
            self.files[file] = None
        self.control_igv = control_igv
        self.output_path = output_path
        self.screen_height = NSScreen.mainScreen().frame().size.height
        self.process()

    def process(self):
        for i, filename in enumerate(self.files):
            self.check_image(filename=filename)


    def check_image(self, filename):
        image = cv2.imread(filename)
        image_name = os.path.basename(filename)
        is_positive = self._check(image, image_name)
        return image_name, is_positive


    def _check(self, image, image_name):
        cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)
        while True:
            height, width = image.shape[:2]
            scaling_f = height / self.screen_height
            small = cv2.resize(image, None, fx=1 / scaling_f, fy=1 / scaling_f)
            # display the image and wait for a keypress
            cv2.imshow(image_name, small)
            key = cv2.waitKey(1)

            # if the 'y' key is pressed return True
            if key == ord("y"):
                cv2.destroyWindow(image_name)
                print('True')
                return True

            # if the 'n' key is pressed return False
            elif key == ord("n"):
                print('False')
                cv2.destroyWindow(image_name)
                return False

            # if the 'm' key is pressed return Maybe
            elif key == ord("m"):
                print('Maybe')
                cv2.destroyWindow(image_name)
                return 'Maybe'


@click.command()
@click.argument('files',
                nargs=-1, type=click.Path(exists=True))
@click.option('--output_path',
              help='Write result here',
              default=None,
              type=click.Path(exists=False))
@click.option('control_igv/no_control_igv',
              help='Control IGV by clicking on image?',
              default=True)
def check_files(**kwds):
    CheckImages(**kwds)


if __name__ == "__main__":
    check_files()
