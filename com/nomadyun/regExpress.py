# -*- coding: utf-8 -*-
'''
Created on 2014年10月9日

@author: nomadyun
'''
import re
line = 'stream-01-31/247.ts'
p_ts = re.compile(r'(.*)/(.*.ts)')
match = p_ts.search(line)
if match:
    print match.group()
    print match.group(1)
    print match.group(2)
else:
    print 'NOT match'
print '\n'



#case 1:
patten = re.compile(r'world')
match = patten.search('hello worlddd')
if match:
    print match.group()
else:
    print 'NOT match'
print '\n'

#case 2:
m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
print "m.string:", m.string                 #m.string:hello world!
print "m.re:", m.re                         #m.re: <_sre.SRE_Pattern object at 0x02019930>
print "m.pos:", m.pos                       #m.pos:0
print "m.endpos:", m.endpos                 #m.pos:12
print "m.lastindex:", m.lastindex           #m.lastindex:3
print "m.lastgroup:", m.lastgroup           #m.lastgroup:sign
 
print "m.group(1,2):", m.group(1, 2)        #m.group(1,2):('hello' 'world')
print "m.groups():", m.groups()             #m.groups():('hello' 'world' '!')
print "m.groupdict():", m.groupdict()       #m.groupdict():{'sign':'!'}
print "m.start(2):", m.start(2)             #m.start(2):6
print "m.end(2):", m.end(2)                 #m.end(2):11
print "m.span(2):", m.span(2)               #m.span(6,11):
print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')#m.expand(r'\2 \1\3'):world hello!
print '\n'

#case 3:
p = re.compile(r'\d+')
print p.split('one1two2three3four4')
print '\n'

#case 4:
p = re.compile(r'\d+')
print p.findall('one1two2three3four4')
print '\n'

#case 5:
p = re.compile(r'\d+')
for m in p.finditer('one1two2three3four4'):
    print m.group(),
print '\n'

#cse 6:
p = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'
print p.sub(r'\2 \1', s) 
def func(m):
    return m.group(1).title() + ' ' + m.group(2).title() 
print p.sub(func, s)
print '\n'

#case 7:
testStr = 'an example word:cat!!'
match = re.search(r'word:\w\w\w', testStr)
    # If-statement after search() tests if it succeeded 
if match:                    
    print 'found', match.group() ## 'found word:cat'
else:
    print 'did not find'
print '\n'

#case 8
testStr = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
tuples = re.findall(r'([\w\.-]+)@([\w\.-]+)', testStr)
print tuples  ## [('alice', 'google.com'), ('bob', 'abc.com')]
for tuple_test in tuples:
    print tuple_test[0]  ## username
    print tuple_test[1]  ## host

#case 7:
patten = re.compile(r'(?<=notificationUrl":")/auth/service\?userId=\d+&_sign=\S+&session=\S+&nonce=\S+(?="})')
testStr = '&&&START&&&{"passToken":"Aq3FBlXT880Y+FyC7LB8rZZL3qvBp0qYAWBPZ+2O2lI1iuaN70mPhvBR427XDZVes+JioVwvq6nf+VzP5cso4BKqf9k/sX3ROMwQJ2zTw+MqWDIrD6gdozISEStEmMg4AoOfMnBz9NjuaBFiE238Ab5svXmVSPM6vOutZeEklh+jD8Yi4m2wGr5RlTZthfeSaScrdm2ylKIWa5aW6vd53nzr+SIRNHNQwMcT8hiTGm8=","securityStatus":16,"ssecurity":"JiLJoJZ0V+pKur2Xj4kWHA==","desc":"成功","nonce":6818559300402877440,"location":"/auth/service?userId=165693048&_sign=Yb2ztWBjFaFZ7lR0dnYaElJ9o7E%3D&session=E12ZWzATBXTopRtNppTzg3SSeQmNM4RUWlFMdZ6EzRJckFqzFwHesapr2%2Ft9rqwuPGhCydX2gio1XvBSvCfZOfABD2phOgeZ2bgUtGA59JaBv0wyvLd%2BCizZri7tMQKgGcr7mqlU8jSXSXIWfLgJYxsH0KnJoFiR4f227bdnVRxnsrrL3lPaEuhhw%2FjQvSdKRh%2FBQNgnipPN0Rxw99g5Qg%3D%3D&nonce=SoetMcsln%2FwBaXp4","userId":165693048,"captchaUrl":null,"psecurity":"ZE9GLU0c/IRDDcd+E0oWaw==","code":0,"qs":"%3Fsid%3Dpassport","notificationUrl":"/auth/service?userId=165693048&_sign=Yb2ztWBjFaFZ7lR0dnYaElJ9o7E%3D&session=E12ZWzATBXTopRtNppTzg3SSeQmNM4RUWlFMdZ6EzRJckFqzFwHesapr2%2Ft9rqwuPGhCydX2gio1XvBSvCfZOfABD2phOgeZ2bgUtGA59JaBv0wyvLd%2BCizZri7tMQKgGcr7mqlU8jSXSXIWfLgJYxsH0KnJoFiR4f227bdnVRxnsrrL3lPaEuhhw%2FjQvSdKRh%2FBQNgnipPN0Rxw99g5Qg%3D%3D&nonce=SoetMcsln%2FwBaXp4"}'
match = patten.search(testStr)
    # If-statement after search() tests if it succeeded 
if match:                    
    print 'found', match.group() ## 'found word:cat'
else:
    print 'did not find'
print '\n'
