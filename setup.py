#!/usr/bin/env python

import sys
from setuptools import setup

sys.path.insert(0, 'libcnml')
from version import __version__, __license__
sys.path.remove('libcnml')

if sys.argv[-1] == 'publish':
    import os
    os.system("python setup.py sdist bdist_wheel upload -s")
    args = {'version': __version__}
    print("You probably want to also tag the version now:")
    print("  git tag -s -a v%(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

setup(
    name='libcnml',
    packages=['libcnml'],
    version=__version__,
    description="A CNML parser for Python",
    long_description=open('README.md').read(),
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    url='https://github.com/PabloCastellano/libcnml/',
    download_url='https://github.com/PabloCastellano/libcnml/archive/master.zip',
    keywords = ['cnml', 'free networks', 'guifi.net'],
    license=__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['six'],
    test_suite = "libcnml.tests.test_libcnml"
)
