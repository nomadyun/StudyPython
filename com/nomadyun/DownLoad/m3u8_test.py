#-*- coding:utf-8 -*-
'''
Created on 2014-12-15

@author: nomadyun
'''
import m3u8
base_url = 'https://devimages.apple.com.edgekey.net/streaming/examples/bipbop_16x9/bipbop_16x9_variant.m3u8'
variant_m3u8 = m3u8.load(base_url)  # this could also be an absolute filename
if variant_m3u8.is_variant:
    for playlist in variant_m3u8.playlists:
        print playlist.uri
        print playlist.stream_info.bandwidth

if __name__ == '__main__':
    pass