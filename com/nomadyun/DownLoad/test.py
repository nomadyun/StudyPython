# -*- coding:utf-8 -*-
'''
Created on 2015-09-19
Test
@author: huang_yun
'''

import re, os, threading, time
import urllib, urllib2

#max_thread = 10
# 初始化锁
#lock = threading.RLock()

# import socket
# socket.setdefaulttimeout(5.0)
# URI="01-iframe.m3u8"
p_m3u8 = re.compile('0\d.m3u8')
# stream-01-31/247.ts
p_ts = re.compile(r'(.*)/(.*.ts)')

down_path = 'F:/HLS_Download'
baseUrl = 'http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/1240_vod.m3u8'
urlRoot = 'http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/'

m3u8_list = []
ts_list = []
filelist = []
def M3U8Paser(URI):
    req = urllib2.Request(URI)
    try: 
        response = urllib2.urlopen(req, timeout=10)
    except urllib2.URLError, e:        
        if hasattr(e, 'code'):            
            print 'The server couldn\'t fulfill the request.'           
            print 'Error code: ', e.code          
        elif hasattr(e, 'reason'):           
            print 'We failed to reach a server.'           
            print 'Reason: ', e.reason    
    else:    
        content = response.readlines()
        for line in content:
            m_m3u8 = p_m3u8.search(line)
            m_ts = p_ts.search(line)
                        
            if m_m3u8:
                m3u8_list.append(m_m3u8.group(0))
                # print line
                sub_m3u8 = m_m3u8.group(0)
                sub_m3u8_url = urlRoot + sub_m3u8
                print sub_m3u8_url
                M3U8Paser(sub_m3u8_url)                    
            elif m_ts:           
                ts_list.append(m_ts.group(0))
                # print ts_list
                ts = m_ts.group(0)
                sub_dir = m_ts.group(1)                
                global ts_name 
                ts_name = m_ts.group(2)                
                ts_url = urlRoot + ts
                filelist.append(ts_url)
                dir_name = os.path.join(down_path, sub_dir)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                os.chdir(dir_name)
                print 'Files will be downloaded to:' + '' + os.getcwd()        
                print 'Downloading:' + ts             
                t = downloader(ts_url, ts_name)
                time.sleep(1)
                threads.append(t)
                t.start()  
class downloader(threading.Thread):
        def __init__(self, url, name):
            threading.Thread.__init__(self)
            self.url = url
            self.name = name

        def run(self):
            print 'downloading %s' % self.url
            f = open(self.name, 'wb') 
            urllib.urlretrieve(self.url, self.name)
            print 'download complete %s' % self.name            
            f.close()

threads = []

if __name__ == '__main__':
    M3U8Paser(baseUrl)
    for t in threads:
        t.setDaemon(True)    
        t.join()   
