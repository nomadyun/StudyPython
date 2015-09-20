#-*- coding:utf-8 -*-
'''
Created on 2015-09-19

@author: huang_yun
'''

import re,os
import urllib,urllib2

p_m3u8 = re.compile('.*.m3u8')
p_ts = re.compile('.*.ts')

down_path = 'F:/HLS_Download'
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
        #m_m3u8 = p_m3u8.search(line)
        print line    
    #print res
   
    for line in res:
        m_m3u8 = p_m3u8.search(line)
        print line
        m_ts = p_ts.search(line)
        if m_m3u8:
            m3u8_list.append(m_m3u8.group(0))
        elif m_ts:
            ts_list.append(m_ts.group(0))
    print m3u8_list
    return ts_list   
      
def download_ts(URI):
    if not os.path.exists(down_path):
        os.makedirs(down_path)
    os.chdir(down_path)
    print 'Files will be downloaded to:' + '' + os.getcwd()
    
    TS_Files = M3U8Paser(URI)
    for filename in TS_Files:
        tsURL = urlRoot + filename
        print 'Downloading:' + filename
        urllib.urlretrieve(tsURL,filename)

if __name__ == '__main__':
    #download_ts(baseUrl)
    M3U8Paser(baseUrl)