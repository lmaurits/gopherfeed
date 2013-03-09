#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from gopherfeed import __version__ as version

setup(
    name='gopherfeed',
    version=version,
    description='Convert RSS or Atom feeds to gophermap files',
    author='Luke Maurits',
    author_email='luke@maurits.id.au',
    url='https://github.com/lmaurits/gopherfeed',
    license="BSD (3 clause)",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
    ],
    scripts=['bin/gopherfeed',],
    py_modules=['gopherfeed',],
    requires=['feedparser'],
    install_requires=['feedparser']
)
