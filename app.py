#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

# Required:
#  $ pip install beautifulsoup4
#  $ pip install lxml

from bs4 import BeautifulSoup
import configparser
import urllib.request


def get_baseurl():
    config = configparser.ConfigParser()
    config.read('example.ini')
    config.sections()
    if 'urls' in config:
        return config['urls']['pref_index']
    else:
        return ''


def main(url):
    if url and url.startswith('http'):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read()
        print(html)
        soup = BeautifulSoup(html, 'lxml')


if __name__ == '__main__':
    base_url = get_baseurl()
    main(base_url)
