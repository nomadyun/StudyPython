#-*- coding:utf-8 -*-
'''
Created on 2015-09-19
Test
@author: huang_yun
'''

import re,os
import urllib,urllib2
#URI="01-iframe.m3u8"
p_m3u8 = re.compile('.*.m3u8')
#stream-01-31/247.ts
p_ts = re.compile(r'(.*)/(.*.ts)')

down_path = 'J:/HLS_Download'
baseUrl = 'http://213.65.40.18:8090/session/8b57ea72-5de9-11e5-ae49-984be10b109c/wp5abc/\
c_116_hls_fuel_tv_abf4730f4fedc76717a6298e907e4019/index.m3u8?token=f9238d3442d7ee8efac65e701bd702fa_1442641333'

urlRoot = 'http://213.65.40.18:8090/session/8b57ea72-5de9-11e5-ae49-984be10b109c/wp5abc/\
c_116_hls_fuel_tv_abf4730f4fedc76717a6298e907e4019/'

def M3U8Paser(URI):
    m3u8_list = []
    ts_list = []
    content = urllib2.urlopen(URI)   
    res = content.readlines()
   
    for line in res:
        m_m3u8 = p_m3u8.search(line)
        print line
        m_ts = p_ts.search(line)
        
        if m_m3u8:
            m3u8_list.append(m_m3u8.group(0))
            sub_m3u8 = m_m3u8.group(0)
            sub_m3u8_url = urlRoot + sub_m3u8
            M3U8Paser(sub_m3u8_url)
        elif m_ts:
            ts_list.append(m_ts.group(0))
    print m3u8_list
    return ts_list   
      
def download_ts(URI):
    '''
    if not os.path.exists(down_path):
        os.makedirs(down_path)
    os.chdir(down_path)
    print 'Files will be downloaded to:' + '' + os.getcwd()
    '''
    TS_Files = M3U8Paser(URI)
    for ts_file in TS_Files:
        m_ts = p_ts.search(ts_file)
        sub_dir = m_ts.group(1)
        ts_name = m_ts.group(2)
        if not os.path.exists(down_path/sub_dir):
            os.makedirs(down_path/sub_dir)
        os.chdir(down_path/sub_dir)
        print 'Files will be downloaded to:' + '' + os.getcwd()        
        tsURL = urlRoot + ts_file
        print 'Downloading:' + ts_file
        urllib.urlretrieve(tsURL,ts_name)

if __name__ == '__main__':
    #download_ts(baseUrl)
    M3U8Paser(baseUrl)