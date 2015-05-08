#!/usr/bin/env python

from setuptools import setup

VERSION = '0.8'

setup(
    name='libcnml',
    packages=['libcnml'],
    version=VERSION,
    description="A CNML parser for Python",
    long_description=open('README.md').read(),
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    url='https://github.com/PabloCastellano/libcnml/',
    download_url='https://github.com/PabloCastellano/libcnml/archive/master.zip',
    keywords = ['cnml', 'free networks', 'guifi.net'],
    license='GPLv3+',
    data_files=[('', ['LICENSE.txt'])],
    include_package_data=True,
    zip_safe=False,
    install_requires=['six'],
    test_suite = "libcnml.tests.test_libcnml"
)
