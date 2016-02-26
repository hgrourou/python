# -*- coding:utf-8 -*-
#! /opt/python3.3.2/bin/python3.3
import urllib.request
import re
import os
import sys
import time
import xml.etree.ElementTree as ET
true=1
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
#print (pwd)
#print (pwd1)
#print (pwd2)
while true:
	#获取含有COUNT的页面
	url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=soybean+qtl&retmax=20"
	headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
	opener = urllib.request.build_opener()
	opener.addheaders = [headers]
	doc = opener.open(url).read()
	data=doc.decode('utf-8') #= "http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
	h=open("../download/new.xml","w")
	h.write(data)
	h.close()

	#获取新页面下的COUNT
	data=open("../download/new.xml").read()
	pattern=re.compile("<Count>.*</Count>")# 正则表达式匹配链接
	m=pattern.search(data)
	str1=m.group()
	str=str1[7]+str1[8]+str1[9]+str1[10]+str1[11]
	print (str)


	#比较COUNT是否相同
	count=open('../download/count.txt').read()
	if count==str: 
		print ('yes')
		time.sleep(7200)
	else :
		print ('no')
		h1=open('../download/count.txt','w')
		h1.write(str)
		h1.close()
		#获取新的PMCID号的页面
		url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=soybean&retmax=100000"
		headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
		opener = urllib.request.build_opener()
		opener.addheaders = [headers]
		doc = opener.open(url).read()
		data=doc.decode('utf-8') #= "http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
		h=open("../download/new2.xml","w")
		h.write(data)
		h.close()

		#获取新的PMID号
		file=open('../download/pmc2.txt','w')
		tree = ET.parse('../download/new2.xml')
		root = tree.getroot()
		tags = root.findall(".//Id")
		#pcs = tag.findall("Id")
		for tag in tags:
			#print(tag.text)
			file.write('PMC'+tag.text+'\n')
		file.close()



		#比较新的PMID号和旧的不同之处,不同的输出
		os.system('./shuchupmc.sh')

		#提取出来PMCID,保存到C3.txt中
		data=open('../download/c.txt','r').read()
		pattern=re.compile("PMC.*")# 正则表达式匹配链接
		file=open('../download/c2.txt','w')
		file.write("".join(re.findall(pattern,data)))
		file.close()
		data2=open('../download/c2.txt','r').read()
		#print (data2)
		data3=re.sub("P","\nP",data2)
		h1=open('../download/c2.txt','w')
		h1.write(data3)
		#data2.close()
		h1.close()
		h2=open('../download/c2.txt','r')
		file_text=h2.read()
		h2.close()
		file_text=file_text.split()
		file_text='\n'.join(file_text)
		h3=open('../download/c3.txt','w')                
		h3.write(file_text)       
		h3.close()


		#根据PMCID号获取html文件,并获得下载链接
		myfile=open("../download/c3.txt","r")
		while True:
			line=myfile.readline().strip('\n')
			if line:
				url =" http://www.ncbi.nlm.nih.gov/pmc/articles/"+line
				headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
				opener = urllib.request.build_opener()
				opener.addheaders = [headers]
				doc = opener.open(url).read()
				data=doc.decode('utf-8')
				#html=open("../html/"+line+".html","w")
				#if len(sys.argv)>2:
					#html=open(pwd1+line+".html","w")
				#else :
				html=open(pwd1+line+".html","w")
				html.write(data)
				html.close()

				pattern=re.compile("/pmc/articles/"+line+"/pdf/.*pdf")# 正则表达式匹配链接
				m=pattern.search(data)
				str2="http://www.ncbi.nlm.nih.gov"
				str1=m.group()
				str3=str2+str1
				f=open("../download/gengxin.txt","a")#存放下载链接
				f.write(str3)
				f.write("\n")
				f.close()
		
			else:
				 break;
		myfile.close()
		#下载pdf文件
		os.system('./gengxin.sh ' + pwd2)
		
