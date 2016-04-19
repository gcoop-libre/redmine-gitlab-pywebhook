#!/usr/bin/env python
from setuptools import setup

setup(
    name='redmine-gitlab-pywebhook',
    version='0.1.0',
    description='A simple gitlab webhook to integrate redmine issues tracker',
    author='Luciano Rossi',
    author_email='lukio@gcoop.coop',
    install_requires=['setuptools', 'python-redmine', 'Flask', 'Flask-ini'],
    packages=['redmine-gitlab-pywebhook'],
    url='http://www.gcoop.coop',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
    license='GPL-3',
)
