#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
from setuptools import setup, Extension

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
requirements = ["jmespath>=0.9.3,<1.0.0"]

setup(
    name="JMESpand",
    url="https://github.com/rickardp/jmespand",
    author="Rickard Lyrenius",
    author_email="rickard@evolviq.com",
    version="0.1.1",
    description="Configuration template expansion system using JMESpath",
    packages=['jmespand'],
    install_requires=requirements + test_requirements,
    zip_safe=True,
    test_suite='tests',
    classifiers=[
        "License :: OSI Approved :: Apache Software License", 
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers"]
)