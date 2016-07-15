Release Notes / Changelog
=========================

For the most accurate detail, we recommend you review the git log.

Version 1.0 [unreleased]
------------------------

- TODO

Version 0.9.5 [2016-07-15]
--------------------------

- FIX: bug when calling CNMLParser with lazy=True and validate=False
- FIX: Assign correctly interfaces that are children of radios (issue #13)
- NEW: Added support for CNML type "node"
- NEW: Manage new attribute "mainipv4" in CNML and DTD
- NEW: Parse new attributes: CNMLNode.zone, CNMLRadio.snmp_index, CNMLDevice.mainipv4
- NEW: Added a bunch of getters to CNMLParser, CNMLZone, CNMLNode and more.
- IMP: Add CNMLService to its own CNMLDevice (issue #8)
- IMP: Expose validate on CNMLParser.__init__
- IMP: Renamed CNMLInterface.parentRadio to parent since it can be a CNMLDevice too
- IMP: CNMLService: attributes created and updated (added) are datetime objects
- IMP: Renamed functions to more Pythonic names (+ added deprecation warnings)
- IMP: Important code cleaning

Version 0.9.4 [2016-01-27]
--------------------------

- Removed shebang (issue #17)

Version 0.9.3 [2016-01-11]
--------------------------

- Implemented __str__() methods
- Some fixes to ease packaging in linux distros (issue #14)

Version 0.9.2 [2015-05-11]
--------------------------

- CNMLLink: status is now libcnml.Status
- Removed NEWS (replaced by CHANGES.rst)
- Added README.md to MANIFEST.in. It was preventing the egg package from being installed

Version 0.9.1 [2015-05-10]
--------------------------

- Fixed bug in some cases when decoding URLs
- Added more tests
- Parse more attributes (created, updated, antenna_elevation)
- New methods: get_inner_links() and get_outer_links()

Version 0.9 [2015-05-08]
------------------------

- Fixed minidom errors
- `#1 <https://github.com/PabloCastellano/libcnml/pull/1>`_: Added possibility to load CNML from URL in ``CNMLParser``

Version 0.8 [2014-10-26]
------------------------

- Release 0.8
- Support new "inactive" status
- Added new Status.get_status_list() static method
- Parsing improvements
- Use logging library instead of prints
- Python 3 changes
- Better documentation
- Tests suite
- Include DTD
- Moved from Gitorious to GitHub and changed references

Version 0.7 [2013-02-07]
------------------------

- Release 0.7
