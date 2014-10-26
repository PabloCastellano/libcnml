#!/usr/bin/env python

from setuptools import setup

VERSION = '0.8'

setup(
    name='libcnml',
    packages=['libcnml'],
    version=VERSION,
    description="A CNML parser for Python",
    long_description=open('README.txt').read(),
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    url='https://github.com/PabloCastellano/guifinetstudio',
    download_url='https://github.com/PabloCastellano/guifinetstudio/releases/tag/libcnml_0.8',
    keywords = ['cnml', 'free networks', 'guifi.net'],
    license='GPLv3+',
    data_files=[('', ['LICENSE.txt'])],
    include_package_data=True,
    zip_safe=False,
    test_suite = "libcnml.tests.test_libcnml"
)
