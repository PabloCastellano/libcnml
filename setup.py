#!/usr/bin/env python

from distutils.core import setup

VERSION = '0.7'

setup(
    name='libcnml',
    version=VERSION,
    description="A CNML parser for Python",
    long_description=open('README.txt').read(),
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    packages=['libcnml'],
    license='GPLv3+',
    data_files=[('', ['LICENSE.txt'])],
    include_package_data=True,
    zip_safe=False,
)
