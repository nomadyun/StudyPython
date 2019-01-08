# -*- coding:utf-8 -*-
import validators
import urllib.request
import urllib.parse
from urllib.error import URLError
import m3u8
import os
import re
import threading
import time

dl_basedir = 'F:\Temp\download_test'

url_patten = re.compile(r'http(s?)://.*\b(?=")?')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}


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
            return response
        except URLError as e:
            if hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.' + uri)
                print(('HTTPError code: ', e.code))
            elif hasattr(e, 'reason'):
                print('Failed to reach the server.' + uri)
                print(('URLError: ', e.reason))
            exit()


class UrlResponse:
    def __init__(self, uri, response):
        self.uri = uri
        self.response = response

    def get_content(self):
        content = self.response.read()
        return content

    def get_final_url(self):
        response_url = self.response.geturl()
        url_parsed = urllib.parse.urlparse(response_url)
        uri_parts = [url_parsed.scheme, url_parsed.netloc, url_parsed.path, "", "", ""]      # remove query,token etc.
        final_url = urllib.parse.urlunparse(uri_parts)
        return final_url

    def get_filename(self):
        final_url = self.get_final_url()
        filename = os.path.basename(final_url)
        return filename


def get_file_name(uri):
    response = available_url(uri)
    response = UrlResponse(uri, response)
    filename = response.get_filename()
    return filename


class MasterM3u8:
    def __init__(self, uri):
        self.uri = uri

    def get_master_baseuri(self):
        master_base_uri = os.path.dirname(self.uri)
        return master_base_uri

    def get_master_dlpath(self):
        m3u8_base_uri = self.get_master_baseuri()
        m3u8_base_path = os.path.basename(m3u8_base_uri)  # get the last path of the m3u8 path
        print("Master M3u8 Path: " + m3u8_base_path)
        master_dl_path = os.path.join(dl_basedir, m3u8_base_path)
        return master_dl_path


class ParsePlaylist:
    def __init__(self, m3u8_obj):
        self.m3u8_obj = m3u8_obj

    # if EXT-X-MAP
    def get_segment_map(self):
        if self.m3u8_obj.segment_map:
            segment_map = self.m3u8_obj.segment_map
            # dict m3u8_obj.segment_map's value of  key 'uri'
            segment_map_uri = segment_map['uri']
            match = url_patten.match(segment_map_uri)
            if match:
                segment_map_path = ''
            else:
                segment_map_path = os.path.dirname(segment_map_uri)
            segment_map_list = (segment_map_uri, segment_map_path)
            return segment_map_list
        else:
            return None

    def get_segments_list(self):
        segments_list = []
        segments = self.m3u8_obj.segments
        for segment in segments:
            segment_uri = segment.uri
            match = url_patten.match(segment_uri)
            if match:
                segment_path = ""
            else:
                segment_path = segment.base_path
            segment_tuple = (segment_uri, segment_path)
            if segment_tuple not in segments_list:
                segments_list.append(segment_tuple)
        return segments_list

    # if EXT-X-KEY:
    # Encryption stream, need add keyid into m3u8.model.py to support widevine
    def get_keys_list(self):
        # if a verimatrix drm stream
        vmx_key_patten = re.compile(r'http(s?)://.*/CAB/keyfile\?r=.*')
        keys = self.m3u8_obj.keys
        keys_list = []
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
                elif key.method == "AES-128":
                    print("It\'s a AES-128 stream,will try to download the key.")
                    key_uri = key.uri
                    match = url_patten.match(key_uri)
                    if match:
                        key_path = ""
                    else:
                        key_path = key.base_path
                    key_tuple = (key_uri, key_path)
                    if key_tuple not in keys_list:
                        keys_list.append(key_tuple)
            return keys_list
        else:
            return None


def is_m3u8_file(content):
    if '#EXTM3U' in content:
        m3u8_obj = m3u8.loads(content)
        print("It\'s a m3u8 file.")
        return m3u8_obj
    else:
        print("It\'s  not a hls stream.")
        return False


def get_stream_list(each_playlist):
    each_stream_list = []
    for each_stream in each_playlist:
        if each_stream.uri:      # Maybe media in segment,it's not a indepedent playlist.
            stream_uri = each_stream.uri
            match = url_patten.match(stream_uri)
            if match:
                stream_path = ""
            else:
                stream_path = each_stream.base_path
            stream_tuple = (stream_uri, stream_path)
            if stream_tuple not in each_stream_list:   # remove duplicate stream
                each_stream_list.append(stream_tuple)
    return each_stream_list


def parse_variant_playlist(m3u8_obj):
    all_playlists = []
    playlists = m3u8_obj.playlists
    iframe_playlists = m3u8_obj.iframe_playlists
    media_playlists = m3u8_obj.media
    print("* * * * * * * * * * * * * * * * * * ")
    print("Start to analyse the master M3U8 file:")
    stream_list = get_stream_list(playlists)
    print("There are " + str(len(stream_list)) + " stream playlists:")
    print(stream_list)
    all_playlists.extend(stream_list)

    if iframe_playlists:
        iframe_list = get_stream_list(iframe_playlists)
        print("There are " + str(len(iframe_list)) + " iframe playlists:")
        print(iframe_list)
        all_playlists.extend(iframe_list)
    else:
        print("There is no iframe playlist.")

    if media_playlists:
        media_list = get_stream_list(media_playlists)
        print("There are " + str(len(media_list)) + " media playlists")
        print(media_list)
        all_playlists.extend(media_list)
    else:
        print("There is no media in m3u8.")
    print("All playlists:")
    print(all_playlists)
    print("* * * * * * * * * * * * * * * * * * ")
    return all_playlists


def variant_m3u8(m3u8_obj):
    if m3u8_obj.is_variant:
        print('It\'s a variant m3u8.')
        playlists = parse_variant_playlist(m3u8_obj)
        return playlists
    else:
        print("It\'s not a variant m3u8.\n")
        return False


def has_absolute_url(files_list):
    for file in files_list:
        file_uri = file[0]
        match = url_patten.match(file_uri)
        if match:
            return True
        else:
            continue
    else:
        return False


def check_dir(path):
    # prepare download directory
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print(e.errno)
    os.chdir(path)


def downloader(uri, dl_path, filename):
    check_dir(dl_path)
    print("\n")
    print(('The file ' + filename + ' will be downloaded to: ' + '' + os.getcwd()))
    urllib.request.urlretrieve(uri, filename)
    print(filename + ' downloading finished.')


def replace_absuri(m3u8_file, renamed_files_list):
    f = open(m3u8_file, 'r', encoding='utf-8')
    lines = f.readlines()
    tmp_m3u8 = m3u8_file + ".tmp"
    f_new = open(tmp_m3u8, 'w', encoding='utf-8')
    for line in lines:
        print(line)
        for renamed_file in renamed_files_list:
            uri = renamed_file[0]
            filename = renamed_file[2]
            print(uri)
            if uri in line:
                line = line.replace(uri, filename)
                break
        f_new.write(line)
    f.close()
    f_new.flush()
    f_new.close()
    os.rename(m3u8_file, m3u8_file + ".bak")
    os.rename(tmp_m3u8, m3u8_file)


def rewrite_m3u8(dl_path, m3u8_name, absuri_download_list):
    os.chdir(dl_path)
    replace_absuri(m3u8_name, absuri_download_list)


def download_master_m3u8(uri, master_dl_path, master_m3u8_name):
    downloader(uri, master_dl_path, master_m3u8_name)


def download_subs_m3u8(playlists, master_base_uri, master_dl_path, master_m3u8_name):
    absuri_download_list = []
    subm3u8_download_list = []
    name_index = 0
    for playlist in playlists:
        uri, path = playlist
        dl_path = os.path.join(master_dl_path, path)
        match = url_patten.match(uri)
        if match:
            abs_uri = uri
            sub_m3u8_name = get_file_name(abs_uri)
            sub_m3u8_name_path = str(name_index) + "_" + os.path.splitext(sub_m3u8_name)[0]
            file = sub_m3u8_name_path + "/" + sub_m3u8_name
            dl_path = os.path.join(dl_path, sub_m3u8_name_path)
            download_tuple = (abs_uri, dl_path, file)
            downloader(abs_uri, dl_path, sub_m3u8_name)
            absuri_download_list.append(download_tuple)
            name_index += 1
        else:
            abs_uri = master_base_uri + "/" + uri
            dl_path = os.path.join(master_dl_path, path)
            response = available_url(abs_uri)
            response = UrlResponse(abs_uri, response)
            sub_m3u8_name = response.get_filename()
            download_tuple = (abs_uri, dl_path, sub_m3u8_name)
            downloader(abs_uri, dl_path, sub_m3u8_name)
            subm3u8_download_list.append(download_tuple)
    if len(absuri_download_list) >= 1:
        rewrite_m3u8(master_dl_path, master_m3u8_name, absuri_download_list)
        subm3u8_download_list.extend(absuri_download_list)
    return subm3u8_download_list


def download_segments(m3u8_obj, base_uri, dl_path, filename):
    name_index = 0
    absuri_download_list = []
    files_list = segments_file_list(m3u8_obj)
    for segment in files_list:
        abs_uri = segment[0]
        match = url_patten.match(abs_uri)
        if match:
            abs_uri = abs_uri
            segment_dl_path = dl_path
            file_name = get_file_name(abs_uri)
            new_file_name = str(name_index) + "_" + file_name
            download_tuple = (abs_uri, segment_dl_path, new_file_name)
            downloader(abs_uri, segment_dl_path, new_file_name)
            absuri_download_list.append(download_tuple)
            name_index += 1
        else:
            segment_dl_path = os.path.join(dl_path, segment[1])
            abs_uri = base_uri + "/" + abs_uri
            file_name = get_file_name(abs_uri)
            downloader(abs_uri, segment_dl_path, file_name)
    if len(absuri_download_list) >= 1:
        rewrite_m3u8(dl_path, filename, absuri_download_list)


def download_variant_segments(playlists, master_base_uri, master_dl_path, master_m3u8_name):
        m3u8_dl_list = download_subs_m3u8(playlists, master_base_uri, master_dl_path, master_m3u8_name)
        for playlist in m3u8_dl_list:
            abs_uri = playlist[0]
            abs_uri_basedir = os.path.dirname(abs_uri)
            dl_path = playlist[1]
            file = playlist[2]
            filename = os.path.basename(file)
            abs_file = os.path.join(dl_path, filename)
            m3u8_obj = m3u8.load(abs_file)
            download_segments(m3u8_obj, abs_uri_basedir, dl_path, filename)


def stream_type(m3u8_obj):
    if m3u8_obj.is_endlist:
        print("It\'s a vod stream.")
    else:
        print("It\'s a live stream.")


def segments_file_list(m3u8_obj):
    playlist_obj = ParsePlaylist(m3u8_obj)
    segment_map_list = playlist_obj.get_segment_map()
    segments_list = playlist_obj.get_segments_list()
    keys_list = playlist_obj.get_keys_list()
    all_files_list = segments_list

    if segment_map_list is not None:
        if segment_map_list not in segments_list:
            all_files_list.append(segment_map_list)
    if keys_list is not None:
        all_files_list.extend(keys_list)
    return all_files_list


def get_all_files(uri):
    response = available_url(uri)
    response = UrlResponse(uri, response)
    final_master_uri = response.get_final_url()
    print("Final master url:" + uri)
    master_m3u8_name = response.get_filename()
    content = response.get_content()
    content = bytes.decode(content)  # http returned content
    m3u8_obj = is_m3u8_file(content)
    playlists = variant_m3u8(m3u8_obj)
    master_m3u8_obj = MasterM3u8(final_master_uri)
    master_base_uri = master_m3u8_obj.get_master_baseuri()
    master_dl_path = master_m3u8_obj.get_master_dlpath()
    download_master_m3u8(uri, master_dl_path, master_m3u8_name)

    if playlists is not False:
        download_variant_segments(playlists, master_base_uri, master_dl_path, master_m3u8_name)
    else:
        download_segments(m3u8_obj, master_base_uri, master_dl_path, master_m3u8_name)


threads = []
maxconnections = 10
semlock = threading.BoundedSemaphore(maxconnections)


class DownLoader(threading.Thread):
    # lock = threading.Lock()
    def __init__(self, uri, dl_path, filename):
        threading.Thread.__init__(self)
        self.uri = uri
        self.dl_path = dl_path
        self.filename = filename

    def run(self):
        print(('downloading %s' % self.uri))
        try:
            urllib.request.urlretrieve(self.uri, self.filename)
        except URLError as e:
            if hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.' + self.uri)
                print(('HTTPError code: ', e.code))
            elif hasattr(e, 'reason'):
                print('Failed to reach the server.' + self.uri)
                print(('URLError: ', e.reason))
                print("Retry it.")
                urllib.request.urlretrieve(self.uri, self.filename)

        print(self.dl_path + self.filename + ' downloading finished.\n')
        semlock.release()


if __name__ == '__main__':
    # for t in threads:
    #     t.join()
    # http://cdnbakmi.kaltura.com/p/243342/sp/24334200/playManifest/entryId/0_uka1msg4/flavorIds/1_vqhfu6uy,1_80sohj7p/format/applehttp/protocol/http/a.m3u8
    # https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_adv_example_hevc/master.m3u8
    # http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multi_language_subs.m3u8

    # https://www.rmp-streaming.com/media/hls/fmp4/hevc/playlist.m3u8
    # redirect url
    # http://live-lh.daserste.de/i/daserste_de@91204/index_2692_av-b.m3u8?sd=10&rebase=on
    # http://rr.webtv.telia.com:8090/114_hls_national_geographics_wild
    # http://194.255.252.203:8090/session/701f229e-e706-11e8-b102-984be10b109c/wp5abc/c_114_hls_nationa_c00e2a0cbc8b26c3f362186769d6f233/index.m3u8?token=d45b91f33d20db63fceeb5be93626673_1542260347_1542260347
    # http://stream1.visualon.com:8082/hls/closedcaption/cc_special/177C_640x480_612K_29f.m3u8
    # http://10.2.64.46:8082/tasklink/61947/content-tc/HLS/AES-128/index-session-key.m3u8
    # https://storage.googleapis.com/shaka-demo-assets/angel-one-widevine-hls/hls.m3u8
    # http://hls.ftgroup-devices.com/video1_wid/m3u8/index.m3u8
    # http://streambox.fr/playlists/sample_aes/index.m3u8
    # https://po1.webtv.telia.com:8090/out/u/23_cmore_first_base.m3u8
    get_all_files("http://stream1.visualon.com:8082/hls/closedcaption/cc_special/177C_640x480_612K_29f.m3u8")
