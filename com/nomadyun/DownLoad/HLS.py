#-*- coding:utf-8 -*-
'''
Created on 2014-12-15

@author: huang_yun
'''


import re,os
import urllib.request, urllib.parse, urllib.error

p_url = re.compile(r'(http(s*)://.+/)(.*.m3u8)')
p_m3u8 = re.compile('.*.m3u8')
p_ts = re.compile('.*.ts')

down_path = 'F:/HLS_Download'
baseUrl = 'http://10.2.68.150/webdav/vods/E_MAS_PC_NOLOGO/index.m3u8'
match = p_url.match(baseUrl)
if match:
    #root of the url
    urlRoot = match.group(1)
    print(urlRoot)
else:
    print('Please check the url!')

def M3U8Paser(URI):
    m3u8_list = []
    ts_list = []
    content = urllib.request.urlopen(URI)
    res = content.readlines()
    for line in res:
        m_m3u8 = p_m3u8.search(line)
        print(line)
        m_ts = p_ts.search(line)
        if m_m3u8:
            m3u8_list.append(m_m3u8.group(0))
        elif m_ts:
            ts_list.append(m_ts.group(0))
    print(m3u8_list)
    return ts_list   
        
def download_ts(URI):
    if not os.path.exists(down_path):
        os.makedirs(down_path)
    os.chdir(down_path)
    print(('Files will be downloaded to:' + '' + os.getcwd()))
    
    TS_Files = M3U8Paser(URI)
    for filename in TS_Files:
        tsURL = urlRoot + filename
        print(('Downloading:' + filename))
        urllib.request.urlretrieve(tsURL,filename)

if __name__ == '__main__':
    #download_ts(baseUrl)
    M3U8Paser(baseUrl)