# -*- coding:utf-8 -*-
import validators
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from urllib.error import URLError
import requests
import m3u8
import os
import re
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
    master_url = uri
    playlists = []
    iframe_playlists = []
    media_lists = []

    # m3u8_content = bytes.decode(is_m3u8_file(uri))
    # variant_m3u8 = m3u8.loads(m3u8_content)
    if is_m3u8_file(uri):
        variant_m3u8 = m3u8.load(uri)
        variant_m3u8_base_uri = variant_m3u8.base_uri
        print("Master_m3u8_base_uri:" + variant_m3u8_base_uri)
        print("Start to analyse the Master M3U8 file:")
        if variant_m3u8.is_variant:
            print('It\'s a variant m3u8.')
            playlist_count = 0
            for playlist in variant_m3u8.playlists:
                playlist_count += 1
                playlist_uri = playlist.absolute_uri
                playlist_path = playlist.base_path
                playlists.append([playlist_uri, playlist_path])
            print("There are " + str(playlist_count) + " playlists:")
            print(playlists)
        else:
            print('It\'s not a variant m3u8.')
            return master_url

        if variant_m3u8.iframe_playlists:
            iframe_playlist_count = 0
            for iframe_playlist in variant_m3u8.iframe_playlists:
                iframe_playlist_count += 1
                iframe_playlist_uri = iframe_playlist.absolute_uri
                iframe_playlist_path = iframe_playlist.base_path
                iframe_playlists.append([iframe_playlist_uri, iframe_playlist_path])
            print("There are " + str(iframe_playlist_count) + " iframe playlists:")
            print(iframe_playlists)
        else:
            print("There is no iframe playlist.")

        if variant_m3u8.media:
            media_list_count = 0
            for media_list in variant_m3u8.media:
                if media_list.uri:
                    media_list_count += 1
                    media_list_uri = media_list.absolute_uri
                    media_list_path = media_list.base_path
                    media_lists.append([media_list_uri, media_list_path])
            print("There are " + str(media_list_count) + " media lists:")
            print(media_lists)
        else:
            print("There is no media in m3u8.")

    return playlists, iframe_playlists, media_lists


def stream_type(m3u8_obj):
    if m3u8_obj.is_endlist:
        print("It\'s a vod stream.")
    else:
        print("It\'s a live stream.")


def segments(m3u8_obj):
    segments_list = []
    # get segments absolute url and sub path
    for segment in m3u8_obj.segments:
        segment_uri = segment.absolute_uri
        segment_path = segment.base_path
        segment_uri_list = [segment_uri, segment_path]
        segments_list.append(segment_uri_list)
    return segments_list

# if EXT-X-KEY:
def Enc_key(m3u8_obj):
    vmx_key_patten = re.compile(r'http(s?)://.*/CAB/keyfile\?r=.*')  # if a verimatrix drm stream
    # Encryption stream, need add keyid into m3u8.model.py to support widevine
    keys = m3u8_obj.keys
    for key in keys:
        if key:
            print(key.uri)
            print(key.method)
            if key.method == "AES-128" and vmx_key_patten.match(key.uri):
                print("It\'s a vmx drm stream,will not download.")
                continue
            elif key.method == "SAMPLE-AES":
                print("It\'s a fairplay drm stream,will not download.")
                continue
            elif key.method == "SAMPLE-AES-CTR":
                print("It\'s a widevine drm stream,will not download.")
                continue
            elif key.method == "AES-128" and not vmx_key_patten.match(key.uri):
                key_list = []
                print("It\'s a AES-128 stream,will try to download the key.")
                key_uri = key.absolute_uri
                key_path = key.base_path
                key__uri_list = [key_uri, key_path]
                key_list.append(key__uri_list)
                return key_list
    else:
        return None


# if EXT-X-MAP
def segment_map(m3u8_obj):
    seg_base_uri = m3u8_obj.base_uri
    if m3u8_obj.segment_map:
        seg_map = m3u8_obj.segment_map
        map_segment = []
        # get the absolute uri of map_segment
        seg_map_uri = seg_base_uri + seg_map['uri']  # dict m3u8_obj.segment_map's value of  key 'uri'
        print("seg_map_uri:" + seg_map_uri)
        map_segment.append(seg_map_uri)      #
        seg_map_path = os.path.dirname(seg_map['uri'])  # path of map_segment
        print(seg_map_path)
        map_segment.append(seg_map_path)   # map_segment[seg_map_uri, seg_map_path]

        if 'byterange' in m3u8_obj.segment_map:
            print("It's a byterange stream.")
            byterange = True
        else:
            byterange = False
        return map_segment, byterange
    else:
        return None


def parse_stream_files(uri):
    m3u8_obj = m3u8.load(uri)
    all_segments_list = []
    stream_type(m3u8_obj)
    segments_list = segments(m3u8_obj)
    segment_map_list = segment_map(m3u8_obj)
    enc_key_list = Enc_key(m3u8_obj)

    if segment_map_list is not None:
        all_segments_list.append(segment_map_list[0])
        if not segment_map_list[1]:
            all_segments_list.append(segments_list)
    else:
        all_segments_list.append(segments_list)

    if enc_key_list is not None:
        all_segments_list.append(enc_key_list)

    return all_segments_list


def get_segments_list(uri):
    all_m3u8_lists = parse_master_playlist(uri)
    all_segments = []
    if type(all_m3u8_lists).__name__ == 'tuple':  # tuple (playlists, iframe_playlists, media_lists)
        print(all_m3u8_lists)
        for sub_m3u8_lists in all_m3u8_lists:
            for each_m3u8 in sub_m3u8_lists:
                print(each_m3u8)
                each_m3u8_url = each_m3u8[0]
                each_m3u8_path = each_m3u8[1]
                if is_m3u8_file(each_m3u8_url):
                    segment_dl_list = []
                    segment_list = parse_stream_files(each_m3u8_url)
                    for each_segment_list in segment_list:
                        if isinstance(each_segment_list[0], list):
                            for each_segment in each_segment_list:
                                each_segment_path = each_segment[1]
                                each_segment_dl_path = os.path.join(each_m3u8_path, each_segment_path)
                                print(each_segment_dl_path)
                                segment = [each_segment[0], each_segment_dl_path]
                                segment_dl_list.append(segment)
                                all_segments.append(segment_dl_list)
                        else:
                            each_segment_path = each_segment_list[1]
                            each_segment_dl_path = os.path.join(each_m3u8_path, each_segment_path)
                            segment = [each_segment_list[0], each_segment_dl_path]
                            segment_dl_list.append(segment)
                            all_segments.append(segment_dl_list)
        print(all_segments)
        return all_segments
    else:
        # if not variant m3u8
        all_segments = parse_stream_files(all_m3u8_lists)
        print(all_segments)
        return all_segments

# class downloader(threading.Thread):
#     def __init__(self, uri, file_name):
#         threading.Thread.__init__(self)
#         self.uri = uri
#         self.file_name = file_name


def check_dir(path, name):
    # prepare download directory
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print(e.errno)
    os.chdir(path)
    print(('The file ' + name + ' will be downloaded to:' + '' + os.getcwd()))


def downloader(uri, dl_path, filename):
    check_dir(dl_path, filename)
    urllib.request.urlretrieve(uri, filename)
    print(filename + ' downlaoding finished.')


def download_playlist(uri):
    # download the master m3u8
    print('Start to downlaod the playlist.')
    master_m3u8_name = os.path.basename(uri)
    uri_path = os.path.dirname(uri)
    split_path = os.path.split(uri_path)
    m3u8_base_path = split_path[1]
    print(m3u8_base_path)
    master_dl_path = os.path.join(dl_baseDir, m3u8_base_path)
    downloader(uri, master_dl_path, master_m3u8_name)

    all_playlists = parse_master_playlist(uri)
    if type(all_playlists).__name__ == 'tuple':  # tuple (playlists, iframe_playlists, media_lists)
        for sub_lists in all_playlists:
            for each_m3u8 in sub_lists:
                print(each_m3u8)
                each_m3u8_url = each_m3u8[0]
                each_m3u8_path = each_m3u8[1]
                each_m3u8_name = os.path.basename(each_m3u8_url)
                sub_dl_path = os.path.join(master_dl_path, each_m3u8_path)
                print(sub_dl_path)
                downloader(each_m3u8_url, sub_dl_path, each_m3u8_name)



def download_segments(uri):
    print('Start to download the segments.')
    all_segments_list = get_segments_list(uri)
    uri_path = os.path.dirname(uri)
    split_path = os.path.split(uri_path)
    m3u8_base_path = split_path[1]
    print(m3u8_base_path)
    master_dl_path = os.path.join(dl_baseDir, m3u8_base_path)
    for segment_list in all_segments_list:
        print(segment_list)
        for segment_dl in segment_list:
            print(segment_dl)
            segment_dl_uri = segment_dl[0]
            sement_name = os.path.basename(segment_dl_uri)
            segment_path = segment_dl[1]
            segment_dl_path = os.path.join(master_dl_path, segment_path)
   #         downloader(segment_dl_uri, segment_dl_path, sement_name)



if __name__ == '__main__':
    # Sdownload_playlist("https://www.rmp-streaming.com/media/hls/fmp4/hevc/playlist.m3u8")
    download_segments("https://www.rmp-streaming.com/media/hls/fmp4/hevc/playlist.m3u8")
