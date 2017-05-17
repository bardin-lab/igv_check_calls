import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__VERSION__ = '0.1.0'

ENTRY_POINTS = '''
        [console_scripts]
        check_calls=igv_check_calls.cli.check_calls:check_files
'''

requirements = ['pyobjc', 'click']

setup(
    name='igv_check_calls',
    version=__VERSION__,
    packages=['igv_check_calls', 'igv_check_calls.cli'],
    description="Inspect IGV screenshots",
    long_description="TODO",
    install_requires=requirements,
    entry_points=ENTRY_POINTS,
    keywords='Bioinformatics',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/bardin-lab/igv_check_calls',
    license='MIT',
    author='Marius van den Beek',
    author_email='m.vandenbeek@gmail.com',
)
