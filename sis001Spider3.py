# coding=utf-8

import urllib2
import re
import string
import urllib
from threading import Thread
import time
import os

class CatchLinks(Thread):
	url = None
	keepRunning = False	#状态标识
	subThreads = []

	def __init__(self,url):
		Thread.__init__(self)
		self.url = url
		self.keepRunning = True
	
	# 获取当前页面所有图片主题的二级链接
	def getLinks(self):
		try:
			respone = urllib2.urlopen(self.url)
			print self.url
		#	print respone
			mainPage = respone.read().decode("gbk")
			#print mainPage
			#f = open('22.html','w+')
			#f.write(mainPage)
			#f.close()
		except:
			print 'Get MainPage failed!'

		#links =  re.findall('</a>]</em>.*?<a href="(.*?)">(.*?)</a></span>',mainPage,re.S) #wangpan
		links =  re.findall('</a>]</em>.*?<a href="(.*?)" style=".*?">(.*?)</a></span>',mainPage)
		return links
		#for item in links:
		#	print item[0]
		#	print item[1]

	#获取子链接下所有图片的url，并下载保存
	def getImgs(self,links):
		for item in links:
			if self.keepRunning == True:
				#print item[0]
				#print item[1]
				title = item[1].replace('/','').replace("'",'')
				#print title
				
				try:
					subPageRespone = urllib2.urlopen('http://68.168.16.158/bbs/' + item[0])
					subPage = subPageRespone.read().decode("gbk").encode("utf-8")
				except:
					print 'Get subPage' + title + 'failed!'

				imgurls = re.findall('<img src="(.*?)" border="0" onclick="zoom\(this\)"',subPage)
				if imgurls ==[]:
					imgurls = re.findall('<img width="\d+" height="\d+" src="(.*?)" border="0" alt="" />',subPage)
				#print imgurls	

				
				t = time.localtime()
				folderName = 'D:/sis/' + str(t.__getattribute__('tm_year')) + '-' + str(t.__getattribute__('tm_mon')) + '-' \
								+ str(t.__getattribute__('tm_mday')) + '-' + '/'
				if not os.path.exists(folderName):
					os.makedirs(folderName)

				for i in range(len(imgurls)):
					if self.keepRunning == True:
						fname = folderName + title + str(i) + '.jpg'	#图片保存路径
						try:
							urllib.urlretrieve(imgurls[i],fname)
						except:
							print 'write file ' + title + ' error'
							print imgurls[i]

	def run(self):
		links = self.getLinks()
		self.getImgs(links)
		print 'done~'

	def quitThreads(self):
		for subThread in self.subThreads:
			subThread.keepRunning = False
			print 'subThread quit'

def quit(threads,startPage):
	for i in range(len(threads)):
		threads[i].quitThreads()
		threads[i].keepRunning = False
		print 'thread %d quit' %(i + startPage)
 	print 'exit'

if __name__ == '__main__':
	url = 'http://68.168.16.158/bbs/forum-230-'
	threads = []
	startPage = 2
	endPage = 6

	for i in range(startPage,endPage+1):	#每一页发起一个线程
		print 'thread %d start' %i
		t = CatchLinks(url + str(i) + '.html')
		#print url + str(i) + '.html'
		t.start()
		threads.append(t)

	while True:
		cmd = raw_input()
		if cmd =='quit':
			quit(threads,startPage)