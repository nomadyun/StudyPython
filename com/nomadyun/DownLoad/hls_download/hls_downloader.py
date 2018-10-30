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
url = 'https://www.rmp-streaming.com/media/hls/fmp4/hevc/v270p_fmp4.m3u8'
# url = 'https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_adv_example_hevc/master.m3u8'
# redirect url
# url = 'http://live-lh.daserste.de/i/daserste_de@91204/index_2692_av-b.m3u8?sd=10&rebase=on'
# url = 'http://rr.webtv.telia.com:8090/114_hls_national_geographics_wild'
# url = 'https://storage.googleapis.com/shaka-demo-assets/angel-one-widevine-hls/playlist_v-0576p-1400k-libx264.mp4.m3u8'

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
    m3u8_content = available_url(uri)[1]  # get return value content
    if b'EXTM3U' in m3u8_content:
        # return m3u8_content
        return True
    else:
        print(uri + " :is not a hls stream.")
        exit()


def parse_master_playlist(uri):
    playlists_url = []
    iframe_playlists_url = []
    media_lists_url = []

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
        else:
            print("There is no iframe playlist in:" + uri)

        if variant_m3u8.media:
            for media_list in variant_m3u8.media:
                if media_list.uri:
                 #   print(media_list)
                    media_list_url = media_list.absolute_uri
                 #   print(media_list_url)
                    media_lists_url.append(media_list_url)
            print("media_lists_url:")
        else:
            print("There is no media in m3u8:" + uri)

    return playlists_url, iframe_playlists_url, media_lists_url


def parse_stream_files(uri):
    map_segment = []
    segments_list = []
    m3u8_obj = m3u8.load(uri)
    file_base_uri = m3u8_obj.base_uri
    print('file_base_uri:' + file_base_uri)

    if m3u8_obj.is_endlist:
        print("It\'s a vod stream.")
    else:
        print("It\'s a live stream.")

    for segment in m3u8_obj.segments:
        segment_uri = segment.absolute_uri
        segment_path = segment.base_path
        segment_uri_list = [segment_uri, segment_path]
        segments_list.append(segment_uri_list)
    # Encryption stream, need add keyid into m3u8.model.py to support widevine
    for key in m3u8_obj.keys:
        if key is not None:
            print(key.uri)
            print(key.method)

    if m3u8_obj.segment_map:
        map_segment_uri = file_base_uri + m3u8_obj.segment_map['uri']  # get dict m3u8_obj.segment_map's value of  key 'uri'
        print(map_segment_uri)
        map_segment.append(map_segment_uri)
        map_segment_path = os.path.dirname(m3u8_obj.segment_map['uri'])
        print(map_segment_path)
        map_segment.append(map_segment_path)

        if 'byterange' in m3u8_obj.segment_map:
            print("It's a byterange list.")
            return map_segment
        else:
            print("It's not a byterange list.")
            return map_segment, segments_list

    else:
        return segments_list

def get_segments_list(uri):
    all_m3u8_lists = parse_master_playlist(uri)
    if type(all_m3u8_lists).__name__ == 'tuple':  # tuple (playlists_url, iframe_playlists_url, media_lists_url)
        for sub_m3u8_lists in all_m3u8_lists:
            for each_m3u8_url in sub_m3u8_lists:
                print(each_m3u8_url)
                if is_m3u8_file(each_m3u8_url):
                    parse_stream_files(each_m3u8_url)
                    print(parse_stream_files(each_m3u8_url))
    else:
        # if not variant m3u8
        print(parse_stream_files(all_m3u8_lists))



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
    get_segments_list("https://storage.googleapis.com/shaka-demo-assets/angel-one-widevine-hls/playlist_v-0576p-1400k-libx264.mp4.m3u8")
