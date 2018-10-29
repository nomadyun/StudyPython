# -*- coding:utf-8 -*-
import validators
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from urllib.error import URLError
import requests
import m3u8
import os
import threading

dl_baseDir = 'F:\Temp\download_test'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}
url = 'https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_adv_example_hevc/master.m3u8'


def is_url(uri):
    result = validators.url(uri)
    if result:
        return True
    else:
        print('It\'s not a valid url')
        exit()


def available_url(uri):
    if is_url(uri):
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
                print('Failed to reach the server.')
                print(('URLError: ', e.reason))
            exit()


def is_m3u8_file(uri):
    data = available_url(uri)
    if b'EXTM3U' in data:
        # return data
        return True
    else:
        print(url + " is not a hls stream.")
        exit()


def master_playlist(uri):
    # m3u8_content = bytes.decode(is_m3u8_file(uri))
    # variant_m3u8 = m3u8.loads(m3u8_content)
    if is_m3u8_file(uri):
        variant_m3u8 = m3u8.load(uri)
        print(variant_m3u8.files)
    #    variant_m3u8_baseUri = variant_m3u8.base_uri
    #    print(variant_m3u8_baseUri)
        if variant_m3u8.is_variant:
            print('It\'s a variant m3u8.')
            for playlist in variant_m3u8.playlists:
                print(playlist)
                print(playlist.base_path)
                print(playlist.uri)

                playlist_url = playlist.absolute_uri
                print(playlist_url)
        else:
            print('It\'s not a variant m3u8.')
            return False

        if variant_m3u8.iframe_playlists:
            for iframe_playlist in variant_m3u8.iframe_playlists:
                print(iframe_playlist)
                print(iframe_playlist.base_path)
                print(iframe_playlist.uri)
                iframe_playlist_url = iframe_playlist.absolute_uri
                print(iframe_playlist_url)
        else:
            print("There is no iframe playlist.")
            return False

        if variant_m3u8.media:
            for media_list in variant_m3u8.media:
                if media_list.uri:
                    print(media_list)
                    print(media_list.base_path)
                    print(media_list.uri)
                    print(media_list.absolute_uri)
        else:
            print("There is no media in m3u8.")
            return False


def check_dir(dl_path):
    # prepare download directory
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
    os.chdir(dl_path)
    print(('The file will be downloaded to:' + '' + os.getcwd()))


def downloader(uri, dl_path, filename):
    check_dir(dl_path)
    urllib.request.urlretrieve(uri, filename)


def download_playlist(uri):
    master_m3u8_name = os.path.basename(url)
    downloader(uri, dl_baseDir, master_m3u8_name)


def download_segment(uri):
    pass


if __name__ == '__main__':
    download_playlist(url)
