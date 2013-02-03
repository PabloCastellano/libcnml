#!/usr/bin/env python

from distutils.core import setup

VERSION = '1.0'

setup(
    name='libcnml',
    version=VERSION,
    description="A CNML parser for Python",
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    packages=['libcnml'],
    include_package_data=True,
    zip_safe=False,
)
