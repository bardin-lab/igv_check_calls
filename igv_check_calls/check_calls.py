"""Goes through a list of images. The user can press 'n' or 'y',
which will cause True or False to be written in the output file as a column next to the filename.
Prerequisite is a functional opencv library (on OSX can be installed by brew install opencv), pyobjc (pip install pyobjc)
and opencv-python
"""

from collections import OrderedDict
import os
import subprocess
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

    def __init__(self, files, control_igv, output_path='output.tsv', igv_name='IGV Snapshot'):
        self.files = [f for f in files]
        self.result = OrderedDict()
        self.igv = IGV() if control_igv else None
        self.igv_name = igv_name
        self.output_path = output_path
        self.screen_height = NSScreen.mainScreen().frame().size.height
        self.current_corrdinates = None
        self.process()
        self.write()

    @property
    def image_number_to_process(self):
        return [i for i, filename in enumerate(self.files) if not filename in self.result]

    def process(self, start=0):
        for i, filename in enumerate(self.files[start:]):
            total_i = i + start
            _, action = self.check_image(filename=filename)
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

    def goto_igv(self, event):
        if event == cv2.EVENT_LBUTTONUP:
            subprocess.call(['open', '-a', self.igv_name])
            self.igv.go(self.current_corrdinates)

    def _check(self, image, image_name):
        cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)
        if self.igv:
            cv2.setMouseCallback(image_name, lambda event, x, y, flags, param: self.goto_igv(event))

        chrom, start, end, _, _ = image_name.rsplit('_', 4)
        self.current_corrdinates = "%s:%s-%s" % (chrom, int(start) - 300, int(end) + 300)
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
                image_name = "\t".join(os.path.basename(filename).rsplit('_', 4))
                out.write(template % (image_name, self.result[filename]))
