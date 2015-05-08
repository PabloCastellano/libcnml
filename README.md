LibCNML
=======

**libcnml** is a CNML parser library for Python.

[![Travis libcnml](https://travis-ci.org/PabloCastellano/libcnml.svg?branch=master)](https://travis-ci.org/PabloCastellano/libcnml)

It was part of the [Guifi.net Studio](https://github.com/PabloCastellano/guifinetstudio) project developed by Pablo Castellano
during Google Summer of Code 2012.

Install
=======

You can install it by typing:

    python setup.py install

or you can get it from PYPI by using pip:

    pip install libcnml

Optionally you can also install lxml (read the note below):

    pip install lxml

lxml
====

lxml Python library does a better memory management and is faster than minidom (default XML library in Python).
If you want to manage big sets of nodes like Guifi.net World zone this definitely makes the difference.

For example, these are the results opening a Guifi.net World zone with more than 17.000 nodes:
Minidom took ~23 seconds and 1,4GB RAM. Guifinetstudio window didn't even appear. I had to reboot my laptop.
Lxml took ~4s and 284MB RAM. Guifinetstudio worked, moving through the map is difficult but possible.

You can test it by your own:

    $ cat cnml1.py
    from libcnml import *
    c = CNMLParser('tests/detail')

    $ time python cnml1.py
    Using lxml which is more efficient
    Loaded OK

    real    0m3.974s
    user    0m3.728s
    sys 0m0.188s

    $ time python cnml1.py
    lxml module not found. Falling back to minidom
    Loaded OK

    real    0m22.984s
    user    0m21.997s
    sys 0m0.868s


License
=======
The code license is GPLv3+
