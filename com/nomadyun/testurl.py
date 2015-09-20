#-*- coding: UTF-8 -*-
import urllib
def wget(url):
    try:
        ufile = urllib.urlopen(url)  ## get file-like object for url
        info = ufile.info()   ## meta-info about the url content
        if info.gettype() == 'text/html':
            print 'base url:' + ufile.geturl()
            text = ufile.read()  ## read all its text
            print text
    except IOError:
            print 'Problem to get url:',url       
if __name__ == '__main__':
    wget('http://www.baidu.com')
