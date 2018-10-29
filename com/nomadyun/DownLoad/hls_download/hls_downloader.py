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
# url = 'https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_adv_example_hevc/master.m3u8'

# redirect url
url = 'http://live-lh.daserste.de/i/daserste_de@91204/index_2692_av-b.m3u8?sd=10&rebase=on'

def is_url(uri):
    result = validators.url(uri)
    if result:
        return True
    else:
        print('It\'s not a valid url:' + uri)
        exit()


def available_url(uri):
    if is_url(uri):
        try:
            req = urllib.request.Request(uri, headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            final_url = response.geturl()  # get the real url
            print('Final Url:' + final_url)
            content = response.read()
            return final_url, content
        except URLError as e:
            if hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.' + uri)
                print(('HTTPError code: ', e.code))
            elif hasattr(e, 'reason'):
                print('Failed to reach the server.' + uri)
                print(('URLError: ', e.reason))
            exit()


def is_m3u8_file(uri):
    data = available_url(uri)[1]  # get return value content
    if b'EXTM3U' in data:
        # return data
        return True
    else:
        print(uri + " is not a hls stream." + uri)
        exit()


def master_playlist(uri):
    playlists_url=[]
    iframe_playlists_url=[]
    media_lists_url=[]

    # m3u8_content = bytes.decode(is_m3u8_file(uri))
    # variant_m3u8 = m3u8.loads(m3u8_content)
    if is_m3u8_file(uri):
        variant_m3u8 = m3u8.load(uri)
    #    variant_m3u8_baseUri = variant_m3u8.base_uri
    #    print(variant_m3u8_baseUri)
        if variant_m3u8.is_variant:
            print('It\'s a variant m3u8.' + uri)
            for playlist in variant_m3u8.playlists:
             #   print(playlist)
                playlist_url = playlist.absolute_uri
             #   print(playlist_url)
                playlists_url.append(playlist_url)
            print("playlists_url:")
            # print(playlists_url)
        else:
            print('It\'s not a variant m3u8.' + uri)
            return uri

        if variant_m3u8.iframe_playlists:
            for iframe_playlist in variant_m3u8.iframe_playlists:
             #   print(iframe_playlist)
                iframe_playlist_url = iframe_playlist.absolute_uri
             #   print(iframe_playlist_url)
                iframe_playlists_url.append(iframe_playlist_url)
            print("iframe_playlists_url:")
            # print(iframe_playlists_url)
        else:
            print("There is no iframe playlist in:" + uri)

        if variant_m3u8.media:
            for media_list in variant_m3u8.media:
                if media_list.uri:
                 #   print(media_list)
                    media_list_url = media_list.absolute_uri
                 #   print(media_list_url)
                    media_lists_url.append(media_list_url)
            print("medea_lists_url:")
         #   print(media_lists_url)
        else:
            print("There is no media in m3u8:" + uri)

    return playlists_url, iframe_playlists_url, media_lists_url


def get_segments_list(uri):
    sub_m3u8 = master_playlist(uri)
    if type(sub_m3u8).__name__ == 'tuple':
   # print(master_playlist(uri))
        for sub_m3u8_list in sub_m3u8:
            for sub_m3u8 in sub_m3u8_list:
                print(sub_m3u8)
                if is_m3u8_file(sub_m3u8):
                    playlist_url_obj = m3u8.load(sub_m3u8)
                    segments = playlist_url_obj.files
                    print(segments)
    else:
       # print(master_playlist(uri))
        playlist_url_obj = m3u8.load(sub_m3u8)
        segments = playlist_url_obj.files
        print(segments)

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
    get_segments_list("https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_adv_example_hevc/tp8/iframe_index.m3u8")
