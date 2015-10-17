#-*- coding:utf-8 -*-
'''
Created on 2015-04-01

@author: huang_yun
'''

import re,os,threading
import urllib.request, urllib.parse, urllib.error

p_url = re.compile(r'(http(s*)://.+/)(.*.m3u8)')
p_m3u8 = re.compile('.*.m3u8')
p_ts = re.compile('.*.ts')
p_key = re.compile('#EXT-X-KEY:METHOD=AES-128,URI="(\d*.key)"')

m3u8_list = []
ts_list = []
key_list = []

down_path = 'F:/HLS_Download/'
baseUrl = 'http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/1240_vod.m3u8'

match = p_url.match(baseUrl)
if match:
    #root of the url
    urlRoot = match.group(1)
    print(urlRoot)
else:
    print('Please check the url!')

#prepare download directory
if not os.path.exists(down_path):
    os.makedirs(down_path)
os.chdir(down_path)
print(('Files will be downloaded to:' + '' + os.getcwd()))

def M3U8Paser(URI):
    req = urllib.request.Request(URI)

    try: 
        response = urllib.request.urlopen(req, timeout=10)

    except urllib.error.URLError as e:        
        if hasattr(e, 'code'):            
            print('The server couldn\'t fulfill the request.')           
            print(('Error code: ', e.code))    
      
        elif hasattr(e, 'reason'):           
            print('We failed to reach a server.')           
            print(('Reason: ', e.reason))    

    else:    
        content = response.readlines()
        for line in content:
            m_m3u8 = p_m3u8.search(line)
            m_ts = p_ts.search(line)
            m_key = p_key.search(line)
            #sub url is m3u8
            if m_m3u8:
                m3u8_list.append(m_m3u8.group(0))
                sub_m3u8 = m_m3u8.group(0)
                sub_m3u8_url = urlRoot + sub_m3u8
                # 创建新线程
                t = downloader(sub_m3u8_url,sub_m3u8)
                # 添加线程到线程列表
                threads.append(t)
                # 开启新线程
                t.start()
                #recursive m3u8 url
                M3U8Paser(sub_m3u8_url)
            #sub url is ts
            elif m_ts:
                ts_list.append(m_ts.group(0))
                ts = m_ts.group(0)
                ts_url = urlRoot + ts
                t = downloader(ts_url,ts)
                threads.append(t)
                t.start()
            #sub url is key        
            elif m_key:
                key_list.append(m_key.group(1))
                key = m_key.group(1)
                key_url = urlRoot + key
                t = downloader(key_url,key)
                threads.append(t)
                t.start()    
        print("Download completed!") 
              
class downloader(threading.Thread):
        def __init__(self, url, name):
            threading.Thread.__init__(self)
            self.url=url
            self.name=name

        def run(self):
            print(('downloading %s' % self.url))
            urllib.request.urlretrieve(self.url, self.name)

threads=[]

if __name__ == '__main__':
    M3U8Paser(baseUrl)
    for t in threads:
        t.setDaemon(True)
        t.join()
    