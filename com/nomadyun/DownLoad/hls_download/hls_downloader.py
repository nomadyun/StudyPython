#-*- coding:utf-8 -*-
import validators
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from urllib.error import URLError
import requests
import m3u8

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}
url = 'http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_16x9/bipbop_16x9_variant.m3u8'


def is_url(url):
    result = validators.url(url)
    if result == True:
        return True
    else:
        print('It\'s not a valid url')


def verify_url(url):
    if is_url(url):
        try:
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read()
            return content
        except URLError as e:
            if hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print(('HTTPError code: ', e.code))
            elif hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print(('URLError: ', e.reason))
            return False


def is_m3u8(url):
    data = verify_url(url)

    if not b'EXTM3U' in data:
        print(url + " is not a m3u8 file.")
    else:
        return data


def hls_master_playlist(url):
    content =  bytes.decode(is_m3u8(url))
    variant_m3u8 = m3u8.loads(content)
    if variant_m3u8.is_variant:
        print('True')
    else:
        print('False')


def download_playlist(uri):
    pass


def download_segment(uri):
    pass


if __name__ == '__main__':
    hls_master_playlist(url)
