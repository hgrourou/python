# -*- coding:utf-8 -*-
#! /opt/python3.3.2/bin/python3.3
import urllib.request
import re
import os
import sys
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time


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

#获取含有PMCID的页面
url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=soybean+qtl&retmax=100000"
headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
doc = opener.open(url).read()
data=doc.decode('utf-8') #= "http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
h=open("../download/pmid.xml","w")
h.write(data)
h.close()


#获取当前文献的总数
data=open("../download/pmid.xml").read()
pattern=re.compile("<Count>.*</Count>")# 正则表达式匹配ID号
#data=doc.decode('utf-8')
m=pattern.search(data)
str1=m.group()
file=open('../download/count.txt','w')
file.write(str1[7])
file.write(str1[8])
file.write(str1[9])
file.write(str1[10])
file.write(str1[11])
file.close()


#获取PMCID号
file=open('../download/pmc.txt','w')
tree = ET.parse('../download/pmid.xml')
root = tree.getroot()
tags = root.findall(".//Id")
#pcs = tag.findall("Id")
for tag in tags:
	#print(tag.text)
	file.write('PMC'+tag.text+'\n')
file.close()
	
#去掉PMC文件中的空行
file=open('../download/pmc.txt','r')
file_text=file.read()
file.close()
file_text=file_text.split()
file_text='\n'.join(file_text)
file=open('../download/pmc.txt','w')                
file.write(file_text)       
file.close()

i=0;
#根据PMCID号获取html文件,并获得下载链接
myfile=open("../download/pmc.txt","r")
while True:
	line=myfile.readline().strip('\n')
	if line:
		url ="http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
		headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
		opener = urllib.request.build_opener()
		opener.addheaders = [headers]
		doc = opener.open(url).read()
		
		i=i+1
		print(i)
		print(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
		data=doc.decode('utf-8')
		html=open(pwd1+line+".html","w")
		html.write(data)
		html.close()

		pattern=re.compile("/pmc/articles/"+line+"/pdf/.*pdf")# 正则表达式匹配链接
		m=pattern.search(data)
		str2="http://www.ncbi.nlm.nih.gov"
		if m:
			str1=m.group()
			str3=str2+str1
			f=open("../download/download.txt","a")#存放下载链接
			f.write(str3)
			f.write("\n")
			f.close()
		else:
			print("没找到")
			print(url)
			continue;
		time.sleep(15)
	else:
		 break;
myfile.close()
#下载pdf文件
os.system('./download.sh ' + pwd2)


