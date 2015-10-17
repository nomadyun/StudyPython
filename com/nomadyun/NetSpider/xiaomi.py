# -*- coding:utf-8 -*-
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import io,gzip,re

patten = re.compile(r'(?<=notificationUrl":")/auth/service\?userId=\d+&_sign=\S+&session=\S+&nonce=\S+(?="})')
account_url = 'https://account.xiaomi.com'
home_url = 'https://account.xiaomi.com/pass/auth/security/home?userId='

class RedirctHandler(urllib.request.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		pass
	def http_error_302(self, req, fp, code, msg, headers):
		pass
#处理cookie,得到一个cookieJar实例
cookieJar = http.cookiejar.LWPCookieJar()
cookieHand = urllib.request.HTTPCookieProcessor(cookieJar)
opener = urllib.request.build_opener(cookieHand,urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

def gzdecode(data) :
	compressedstream = io.StringIO(data)  
	gziper = gzip.GzipFile(fileobj=compressedstream)    
	data2 = gziper.read()   # 读取解压缩后数据   
	return data2



class Mi:
	def __init__(self,filename):
		self.file = filename

	def reader_user(self):
		userfile = self.file
		with open(userfile,'r') as f:
			for line in f:
				string = line.lstrip().split('@')
				if(len(string) != 2):
					print("请检查账号格式:userName@passWord")
				userName = string[0]
				passWord = string[1]
				self.login(userName,passWord)

	def login(self,userName,passWord):
		#登录页面
		login_url = 'https://account.xiaomi.com/pass/serviceLogin'
		#poset地址
		post_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
		main_url = 'http://cart.mi.com/cart/add/2140100017'
		#伪装成firefox浏览器，
		headers = {
		    'Host':'account.xiaomi.com',
		    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
		    'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',            
		    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		    'Accept-Encoding':'gzip, deflate',
		    'Referer':'https://account.xiaomi.com/pass/serviceLogin',
			'Connection':'Keep-Alive',
			'Content-Type':'application/x-www-form-urlencoded'
		}
		#生成post数据，包含登录信息
		postData = {
            'user':userName,
            '_json':'true',             
		    'pwd':passWord,
			'callback':'https://account.xiaomi.com',
		    'sid':'passport',
		    'qs':'%3Fsid%3Dpassport',
		    'hidden':'',
		    '_sign':'KKkRvCpZoDC+gLdeyOsdMhwV0Xg=',
            'serviceParam':'{"checkSafePhone":false}'
		}
		postData = urllib.parse.urlencode(postData)	
		try:
			#urllib2.urlopen(login_url)
			req = urllib.request.Request(url = post_url,data = postData,headers = headers)
			res = urllib.request.urlopen(req)
			for cookie in cookieJar:
				#list转换为string
				cookie = str(cookie)
				print(cookie)
			content = res.read()
			match = patten.search(content)
			# If-statement after search() tests if it succeeded 
			if match:                    
				print('Login Success')
				re_url = account_url + match.group()
				print(re_url)
			else:
				print('Failed to login!')

			#result = res.read()
			#print result
			#self.buying()
		except Exception as e:
			print((str(e)))
		url1 = urllib.request.Request(url = re_url,data = None,headers = headers)
		url1_res = urllib.request.urlopen(url1)
		#url2 = urllib2.urlopen(home_url,timeout = 2)
		page1 = url1_res.read()
		print(page1)
		#print url2.geturl()
		url2 = urllib.request.Request(url = main_url,data = None,headers = headers)
		url2_res = urllib.request.urlopen(url2)
		#url2 = urllib2.urlopen(home_url,timeout = 2)
		#page2 = gzdecode(url2_res.read())
		#print page2
# 	def buying(self):
# 		#小米主页
# 		main_url = 'http://www.mi.com/index.html'
# 		buy_url = "http://cart.mi.com/cart/add/2143800012"
# 		headers = {
# 		    'Host':'cart.mi.com',
# 		    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
# 		    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 		    'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',            
# 		    'Accept-Encoding':'gzip, deflate',
# 		    'DNT':'0'
# 		}
# 		try:
# 			urllib2.urlopen(main_url)
# 			for cookie in cookieJar:
# 				#list转换为string
# 				cookie = str(cookie)
# 				print cookie
# 			req = urllib2.Request(buy_url,None,headers)
# 			res = urllib2.urlopen(req)
# 			#读取页面代码
# 			html = gzdecode(res.read())
# 			print res.info()
# 			print(html)
# 		except Exception,e:
# 			print str(e)
# 		print("成功")

if __name__ == '__main__':
	xm = Mi('xiaomi.txt')
	xm.reader_user()
