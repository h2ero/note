#!/usr/bin/python
#coding=utf-8
import MySQLdb
import urllib2
import threading
import Queue
import os

conn = MySQLdb.connect(host='localhost', user='root', passwd='52486258', charset='utf8')
conn.select_db('weimei')
cursor = conn.cursor()
sql = "SELECT src FROM `spider`"
#sql=sql.decode('utf8','ignore');
try:
    res = cursor.execute(sql)
except Exception, e:
    pass
imgUrlList=cursor.fetchall()

def downloadImg(i,url):
    #获取url后缀
    ext=url.split('/')[-1].split('.')[-1]
    imgPath='img/'+str(i)+'.'+ext
    #判断文件是否存在
    if os.path.exists(imgPath):
        print imgPath,"exits,skip"
    else:
        img=urllib2.urlopen(url).read()
        f=open(imgPath,'w');
        f.write(img)
        f.close()
        print "downloadImg:",i

#设置线程数
WORKERS = 20

class Worker(threading.Thread):
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            item = self.__queue.get()
            if item==None:
                self.__queue.task_done()
                break
            downloadImg(item[0],item[1])
            self.__queue.task_done()


queue = Queue.Queue(0)
#
for i in range(WORKERS):
    Worker(queue).start()
#
i=0
for url in imgUrlList:
    i+=1;
    queue.put((i,url[0]))

#确保队列执行完毕，再执行后面的代码
for i in range(WORKERS):
    queue.put(None)
queue.join()

#关闭数据库连接
cursor.close()
conn.close()
print "all images have downloaded"
