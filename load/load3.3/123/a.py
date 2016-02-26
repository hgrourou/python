# -*- coding:utf-8 -*-
#! /opt/python3.3.2/bin/python3.3
import urllib.request
import re
import os
import sys
import xml.etree.ElementTree as ET
import socket

#判断参数的个数,获得存取文件按的路径
if len(sys.argv)>2:
	print (1)
	pwd1=sys.argv[1]
	pwd2=sys.argv[2]
else:
	#print (0)
	pwd=sys.argv[1]
	pwd1=pwd+'html/'
	pwd2=pwd+'pdf/'
#print(sys.argv)
#print(sys.argv[0])
#print(sys.argv[1])
#print(sys.argv[2])
print (pwd)
print (pwd1)
print (pwd2)



timeout=600#防止超时
socket.setdefaulttimeout(timeout)
myfile=open("../pmc.txt","r")
while True:
	line=myfile.readline().strip('\n')
	if line:
		url ="http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
		headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
		opener = urllib.request.build_opener()
		opener.addheaders = [headers]
		try:
			doc = opener.open(url).read()
		except URLError as e:
			if hasattr(e, 'reason'):
				print('We failed to reach a server.')
				print('Reason: ', e.reason)
			elif hasattr(e, 'code'):
				print('The server couldn\'t fulfill the request.')
				print('Error code: ', e.code)
		else:
			print("good!")
			#print(response.read().decode("utf8"))

			#data=doc.decode('utf-8')
			#html=open(pwd1+line+".html","w")
			#html.write(data)
			#html.close()

			pattern=re.compile("/pmc/articles/"+line+"/pdf/.*pdf")# 正则表达式匹配链接
			m=pattern.search(data)
			str2="http://www.ncbi.nlm.nih.gov"
			if m:
				str1=m.group()
				str3=str2+str1
				f=open("../download.txt","a")#存放下载链接
				f.write(str3)
				f.write("\n")
				f.close()
			else:
				print("没找到")
				print(url)
				continue;
	else:
		 break;
myfile.close()
