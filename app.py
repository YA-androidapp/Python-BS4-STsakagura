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
from const import CONST_PREF_URLS, CONST_KURA_ALL_URLS


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


def get_kura_all_urls(pref_urls):
    print('get_kura_all_urls({})'.format(pref_urls))
    kura_all_urls = []
    for pref_url in pref_urls:
        kura_pref_urls = get_kura_index(pref_url)
        kura_all_urls.append(kura_pref_urls)
    kura_all_urls = [item for m in kura_all_urls for item in m]
    return kura_all_urls


def get_kura_info(kura_url):
    print('get_kura_info({})'.format(kura_url))
    if kura_url and kura_url.startswith('http'):
        req = urllib.request.Request(kura_url)
        response = urllib.request.urlopen(req)
        html = response.read()
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        table = soup.find_all(class_='sakagura-table')
        if 1 == len(table):
            trs = table[0].find_all('tr')
            kura_info = {
                'url': kura_url,
            }
            # TODO
            for tr in trs:
                print(tr)
                tr_key = tr.th.string
                tr_val = ((tr.find_all('td'))[0]).text
                kura_info[tr_key] = tr_val
            print('kura_info: {}'.format(kura_info))
            return kura_info
    return {}


def get_kura_all_infos(kura_all_urls):
    kura_all_infos = []
    for kura_url in kura_all_urls:
        kura_info = get_kura_info(kura_url)
        kura_all_infos.append(kura_info)
    return kura_all_infos


if __name__ == '__main__':
    base_url = get_baseurl()
    # print(base_url)

    # アクセス数抑制のため初回のみ実行して定数化した
    # # pref_urls = get_pref_index(base_url)
    # # kura_all_urls = get_kura_all_urls(pref_urls)
    pref_urls = CONST_PREF_URLS
    kura_all_urls = CONST_KURA_ALL_URLS
    # print(kura_all_urls)

    kura_all_infos = get_kura_all_infos(kura_all_urls)
