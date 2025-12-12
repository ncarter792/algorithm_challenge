# algorithm_challenge
Candidate algorithm challenge package. 

## Background 
Without publically sharing the entire challenge prompt, the ask is to basically implement a method that takes a trie and a set of characters, and returns the fraction of letters
in the list of strings used to build the trie that are members of the target set of characters. 

## Package installation and testing

To develop or run tests for this package (assumes a working development environment with [poetry](https://python-poetry.org/)
installed)::

    git clone https://github.com/ncarter792/algorithm_challenge.git
    cd algorithm_challenge
    poetry install

To run unit tests for this package, change to the package base directory and run::

    pytest

Note - Tests for this package run all of the following: unit tests, doctests, flake8, and mypy. A build directory will 
be generated with test output and coverage reports. 

## Background 
This example implements a classical trie except the value is a count rather than a general value. 
