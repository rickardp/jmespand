# jmespand - Python JMESpath expansion in documents

[![Travis CI status](https://travis-ci.org/rickardp/jmespand.svg)](https://travis-ci.org/rickardp/jmespand)
[![License](https://img.shields.io/github/license/rickardp/jmespand.svg)](https://github.com/rickardp/jmespand/blob/master/LICENSE)
[![PyPi version](https://img.shields.io/pypi/v/jmespand.svg)](https://pypi.python.org/pypi/jmespand/)

## Purpose

This Python module expands a set of documents (`dict`s) with format strings (`{expression}`) using [JMESPath](http://jmespath.org) syntax. The purpose is to use this library in configuration systems to provide
templated configuration sets whose properties can refer to other parts of the configuration (as well as outside scope properties).


## Usage

    doc1 = yaml.load(...)
    >>>{"Hello": "{Value}"}
    doc2 = json.load(...)
    >>>{"Value": "World"}

    root = jmespand.create_root(doc1, doc2)

    print(root.expanded())
    >>>{"Hello": "World", "Value": "World"}

since all the expressive power of JMESPath is available it is possible to do a lot more advanced things such as predicates, indexing, etc.

## Limitations

Currently, expansion is limited to strings only. It is currently not possible to expand entire (sub-)objects.