#-*- coding:utf-8 -*-
'''
Created on 2014年11月20日

@author: huang_yun
'''
import re,io,gzip
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,http.cookiejar
from urllib.error import HTTPError, URLError

#登录后的跳转地址
url_Patten = re.compile(r'http://i.taobao.com/my_taobao.htm\?nekot=\S.{26}')
#从cookie提取_tb_token_
token_Patten = re.compile(r'<Cookie _tb_token_=(\w+) for .taobao.com/>')
#从cookie提取Unix timestamp
time_Patten = re.compile(r'<Cookie uc1=lltime=(\d+)&cookie(.*) for .taobao.com/>')

testurl = 'gotoURL:"http://i.taobao.com/my_taobao.htm?nekot=bm9tYWR5dW4%3D1416903130139"'
#登录地址
loginUrl = 'https://login.taobao.com/member/login.jhtml'
jinbiUrl = 'http://taojinbi.taobao.com/index.htm'
baseApiUrl = 'http://api.taojinbi.taobao.com/json/sign_in_everyday.htm?'

fullurl = ''
_tb_token_ = ''
_time_ = ''
checkCode = 'null'
t = ''
enter_time = ''
ua = ''
_ksTS = '1417574815456_130'
callback = 'jsonp131'
#post请求头部
headers1 = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh,en-us;q=0.7,en;q=0.3',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'X-Requested-With':'XMLHttpRequest',
    'Referer':'https://login.taobao.com/member/login.jhtml',   
    'Connection':'keep-alive',
    'Host':'login.taobao.com',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Pragma':'no-cache',
    'Cache-Control':'no-cache'   
}
headers2 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh,en-us;q=0.7,en;q=0.3',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Connection':'keep-alive',
    'Host':'i.taobao.com'
    #'Host':'taojinbi.taobao.com'
}
#用户名，密码
username = input("Please input your username in taobao: ")
password = input("Please input your password of taobao: ")
postData = {
    'TPL_username':username,
    'TPL_password':password,    
    'TPL_checkcode':'',    
    'loginsite':'0',
    'newlogin':'0',
    #===========================================================================
    # 'TPL_redirect_url':'',    
    # 'from':'tb',
    # 'fc':'default',
    # 'style':'default',
    # 'css_style':'',    
    # 'tid':'XOR_1_000000000000000000000000000000_62504557420E74050873060C',
    # 'support':'000001',
    # 'CtrlVersion':'1,0,0,7',
    # 'loginType':'4',
    # 'minititle':'',    
    # 'minipara':'',    
    # 'umto':'Tb91d030a6b783a903b0cada03ab9d252',
    # 'pstrong':'3',
    # 'llnick':'',    
    # 'sign':'',    
    # 'need_sign':'',    
    # 'isIgnore':'',    
    # 'full_redirect':'',    
    # 'popid':'',    
    # 'callback':'',    
    # 'guf':'',    
    # 'not_duplite_str':'',    
    # 'need_user_id':'',    
    # 'poy':'',    
    # 'gvfdcname':'10',
    # 'gvfdcre':'',    
    # 'from_encoding':'',    
    # 'sub':'',    
    # 'TPL_password_2':'88abf1819273be1841dfd2746ded17ba06eac63a47b4ba0da3ddf500d110c894fa6867345777b0db1fca073d5e587e5826cd81599164baef7ffc68f0eba8b16d0718d23337192e0a4fc781144ecd7ca62afd6b37a19bcd3f0b18d5ede99fc283c72521fe9eb0c48d9365a4e0c4eafb4321de2fcd025edfb536e29b2f38467ebc',
    # 'loginASR':'1',
    # 'loginASRSuc':'1',
    # 'allp':'',    
    # 'oslanguage':'zh',
    # 'sr':'1920*1080',
    # 'osVer':'windows|6.1',
    # 'naviVer':'firefox|31'            
    #===========================================================================
}
postData = urllib.parse.urlencode(postData)

#处理cookie
cookieJar = http.cookiejar.LWPCookieJar()
cookieHand = urllib.request.HTTPCookieProcessor(cookieJar)
opener = urllib.request.build_opener(cookieHand,urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

#解压gzip  
def gzdecode(data) :  
    compressedstream = io.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read()   # 读取解压缩后数据   
    return data2

def login_to_taobao():   
    global fullurl
    #打开登录页面取的cookie
    urllib.request.urlopen(loginUrl)
    
    req = urllib.request.Request(loginUrl,postData,headers1)
    
    try:
        res = urllib.request.urlopen(req)
    except HTTPError as e:
        print('The server could not fulfill the request.')    
        print('Error code: ', e.code)  
    except URLError as e:
        print('We failed to reach a server.')  
        print('Reason: ', e.reason)  
    else:
        for cookie in cookieJar:
            #list转换为string
            cookie = str(cookie)
            match = token_Patten.match(cookie)
            if match:
                _tb_token_ = match.group(1)
                print(_tb_token_)
        
        #result = res.read().decode('gbk')
        result = res.readlines()
        info = res.info()     
        status = res.getcode()
        res.close()
        print(status)       
        print(info)
        #print "Response:", result  
    #登录成功后的跳转地址
        try:
            for line in result:
                match = url_Patten.search(line)
                if match:          
                    fullurl = match.group(0)        
                    print('恭喜，登录成功！')
                    #content = urllib2.urlopen(match.group(0)).read()
                    #print content
                    print(fullurl)
        except:             
            print('登录失败')    
            
def taojinbi():
    global fullurl
    login_to_taobao()
    fullurl = urllib.parse.quote(fullurl, safe=':?=/')
    urllib.request.urlopen(fullurl)
    #urllib2.urlopen(jinbiUrl)
    req = urllib.request.Request(fullurl,None,headers2)
    res = urllib.request.urlopen(req)
    result = res.read()
    con = gzdecode(result)
    for cookie in cookieJar:
        #list转换为string
        cookie = str(cookie)
        match_token = token_Patten.match(cookie)
        match_time = time_Patten.match(cookie)
        if match_token:
            _tb_token_ = match_token.group(1)
            print(_tb_token_)
        elif match_time:
            _time_ = match_time.group(1)
            print(_time_)    
        print(cookie)
    info = res.info()
    status = res.getcode()
    geturl = res.geturl()
    res.close()
    print(status)
    print(geturl)
    print(info)
    print(con)
    res.close()
        
if __name__ == '__main__':
    taojinbi()