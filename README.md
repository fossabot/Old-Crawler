# Swiftea's Open Source Web Crawler

## Master branch :
[![Build Status](https://travis-ci.org/Swiftea/Swiftea-Crawler.svg?branch=master)](https://travis-ci.org/Swiftea/Swiftea-Crawler)
[![Coverage Status](https://coveralls.io/repos/Swiftea/Swiftea-Crawler/badge.svg?branch=master)](https://coveralls.io/r/Swiftea/Swiftea-Crawler?branch=master)
[![Documentation Status](https://readthedocs.org/projects/crawler/badge/?version=master)](https://crawler.readthedocs.org/en/master/)
[![Code Health](https://landscape.io/github/Swiftea/Swiftea-Crawler/master/landscape.svg?style=flat)](https://landscape.io/github/Swiftea/Swiftea-Crawler/master)
[![Requirements Status](https://requires.io/github/Swiftea/Swiftea-Crawler/requirements.svg?branch=master)](https://requires.io/github/Swiftea/Swiftea-Crawler/requirements/?branch=master)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSwiftea%2FOld-Crawler.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FSwiftea%2FOld-Crawler?ref=badge_shield)

## Develop branch :
[![Build Status](https://travis-ci.org/Swiftea/Swiftea-Crawler.svg?branch=develop)](https://travis-ci.org/Swiftea/Swiftea-Crawler)
[![Coverage Status](https://coveralls.io/repos/Swiftea/Swiftea-Crawler/badge.svg?branch=develop)](https://coveralls.io/r/Swiftea/Swiftea-Crawler?branch=develop)
[![Documentation Status](https://readthedocs.org/projects/crawler/badge/?version=develop)](https://crawler.readthedocs.org/en/develop)
[![Code Health](https://landscape.io/github/Swiftea/Swiftea-Crawler/develop/landscape.svg?style=flat)](https://landscape.io/github/Swiftea/Swiftea-Crawler/develop)
[![Requirements Status](https://requires.io/github/Swiftea/Swiftea-Crawler/requirements.svg?branch=develop)](https://requires.io/github/Swiftea/Swiftea-Crawler/requirements/?branch=develop)

## Description

Swiftea-Crawler is an open source web crawler for Swiftea: https://swiftea.ovh.

Currently, it can :
  - Visit websites
    - check robots.txt
    - search encoding
  - Parse them
    - extract data
      - title
      - description
      - ...
    - extract important words
      - filter stopwords
  - Index them
    - in database
    - in inverted-index

## Version

Current version is 1.0.1

## Tech

Swiftea's Crawler uses a number of open source projects to work properly:

- [Python 3](https://www.python.org/)
  - [Reppy](https://github.com/seomoz/reppy)
  - [PyMySQL](https://github.com/PyMySQL/PyMySQL/)
  - [Requests](https://github.com/kennethreitz/requests)
  - [Paramiko](http://www.paramiko.org/)


## Contributing

Want to contribute? Great!

Fork the repository. Then, run:

    git clone --recursive git@github.com:<username>/Swiftea-Crawler.git
    cd Swiftea-Crawler
    git flow init -d
    git flow feature start <your feature>

Then, do work and commit your changes. Finally publish your feature.

    git flow feature publish <your feature>

When done, open a pull request to your feature branch.

### Commit conventions :

#### General
  - Use the present tense
  - Use the imperative mood

#### Examples
  - Add something : "Add feature ..."
  - Update : "Update ..."
  - Improve something : "Improve ..."
  - Change something : "Change ..."
  - Fix something : "Fix ..."
  - Fix an issue : "Fix #123456" or "Close #123456"

License
----

GNU GENERAL PUBLIC LICENSE (v3)

**Free Software, Hell Yeah!**


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSwiftea%2FOld-Crawler.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FSwiftea%2FOld-Crawler?ref=badge_large)