"""Goes through a list of images. The user can press 'n' or 'y',
which will cause True or False to be written in the output file as a column next to the filename.
Prerequisite is a functional opencv library (on OSX can be installed by brew install opencv), pyobjc (pip install pyobjc)
and opencv-python
"""
import click

from igv_check_calls.check_calls import CheckImages


@click.command()
@click.argument('files',
                nargs=-1, type=click.Path(exists=True),
		required=True)
@click.option('--output_path',
              help='Write result here',
              default=None,
              type=click.Path(exists=False))
@click.option('--control_igv/--no_control_igv',
              help='Control IGV by clicking on image?',
              default=True)
@click.option('--igv_name',
              help='The name of your IGV Application window.',
              default='IGV Snapshot')
def check_files(**kwds):
    CheckImages(**kwds)


if __name__ == "__main__":
    check_files()
