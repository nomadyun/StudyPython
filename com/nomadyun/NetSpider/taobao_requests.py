#-*- coding:utf-8 -*-
'''
Created on 2014-12-8

@author: huang_yun
'''
import re
import requests
from requests.exceptions import HTTPError


loginUrl = 'https://login.taobao.com/member/login.jhtml'
#redirect url after login
url_Patten = re.compile(r'http://i.taobao.com/my_taobao.htm\?nekot=\S.{26}')
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
#UserName Password
username = raw_input("Please input your username in taobao: ")
password = raw_input("Please input your password of taobao: ")
postData = {
    'TPL_username':username,
    'TPL_password':password,    
    'TPL_checkcode':'',    
    'loginsite':'0',
    'newlogin':'0'
    }

try:
    r1 = requests.get(loginUrl)
    print r1.request.headers
    r = requests.post(loginUrl,data=postData,headers = headers1)
    re_result = r.text
    print r.status_code
    print re_result
    #===========================================================================
    # try:
    #     match = url_Patten.search(re_result)
    #     if match:          
    #         fullurl = match.group(0)        
    #         print 'Login Sucess'
    #         print fullurl
    #         r2 = s.get(fullurl)
    #         cookies2 = r2.cookies
    #         for cookie in cookies2:
    #             print cookie
    #         result = requests.get(fullurl,cookies = cookies2,headers = headers2)
    #         print result.text
    #     else:
    #         print 'No URL Find'    
    # except:             
    #     print 'Fail to login.'    
    #===========================================================================
except HTTPError as err:
    print 'Network Connect Error' + str(err)
    print r.raise_for_status
 

if __name__ == '__main__':
    pass