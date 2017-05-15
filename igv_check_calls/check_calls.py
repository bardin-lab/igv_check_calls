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


ACTIONS = {121: True,
           110: False,
           109: 'maybe',
           3: 'next',
           2: 'previous'}


class CheckImages(object):
    """Check a series of images, optionally see images in detail in IGV."""

    def __init__(self, files, control_igv, output_path='output.tsv'):
        self.files = [f for f in files]
        self.result = OrderedDict()
        self.control_igv = control_igv
        self.output_path = output_path
        self.screen_height = NSScreen.mainScreen().frame().size.height
        self.process()
        self.write()

    @property
    def image_number_to_process(self):
        return [i for i, filename in enumerate(self.files) if not filename in self.result]

    def process(self, start=0):
        for i, filename in enumerate(self.files[start:]):
            total_i = i + start
            _, action = self.check_image(filename=filename)
            print(action)
            if action in {True, False, 'maybe'}:
                self.result[filename] = action
            if action == 'previous':
                return self.process(start=total_i - 1)
        if len(self.image_number_to_process) > 0:
            self.process(start=self.image_number_to_process[0])

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
            if key in ACTIONS:
                cv2.destroyAllWindows()
                return ACTIONS[key]

    def write(self):
        template = "%s\t%s\n"
        with open(self.output_path, 'w') as out:
            for filename in self.result:
                image_name = "\t".join(os.path.basename(filename).split('_', 3))
                out.write(template % (image_name, self.result[filename]))



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
