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
    config.read('urls.ini')
    config.sections()
    if 'urls' in config:
        return config['urls']['pref_index']
    else:
        return ''


def get_pref_index(url):
    print('get_pref_index({})'.format(url))
    if url and url.startswith('http'):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read()
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        ul = soup.find_all(class_='sakayagura-list')
        if 1 == len(ul):
            pref_links = ul[0].select('li > a')
            pref_urls = [i.get('href') for i in pref_links]
            return pref_urls
    return []


def get_kura_index(url):
    url = url.replace('/./', '/')
    print('get_kura_index({})'.format(url))
    # TODO
    # <table class="sakagura-list"><tbody><tr><td><span class="main"><a href="https://">

    if url and url.startswith('http'):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read()
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        table = soup.find_all(class_='sakagura-list')
        if 1 == len(table):
            kura_links = table[0].select('td > span > a')
            kura_pref_urls = [i.get('href') for i in kura_links]
            return kura_pref_urls
    return []


if __name__ == '__main__':
    base_url = get_baseurl()
    # print(base_url)
    pref_urls = get_pref_index(base_url)
    kura_all_urls = []
    for pref_url in pref_urls:
        kura_pref_urls = get_kura_index(pref_url)
        # print(kura_pref_urls)
        kura_all_urls.append(kura_pref_urls)
    kura_all_urls = [item for m in kura_all_urls for item in m]
    print(kura_all_urls)
