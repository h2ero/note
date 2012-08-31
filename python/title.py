#! /usr/bin/python
#coding=utf-8
import MySQLdb
import threading
import Queue
import re
import urllib2 
import Gzzip

conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')
conn.select_db('weimei');
cursor=conn.cursor()
sql="SELECT id,src FROM `spider`  where is_named!=1"# and id>2900"
#sql=sql.decode('utf8','ignore');
try:
    res=cursor.execute(sql)
except Exception, e:
    pass
imgUrlList=cursor.fetchall()

def downloadImg(id,url):
    global WHERE
    global SQLS
    WHERE+=1
    #print WHERE,"条记录以入库"
    url="http://www.google.com/searchbyimage?image_url="+url
    print url
    res=Gzzip.newOpen(url)
    r=res.read()
    #print r
    #print res.headers
    pattern=r'initialize\((.*?)\)'
    url=re.findall(pattern,r,re.MULTILINE|re.S)
    url=url[0].replace('/search','http://www.google.com/search').replace('\\x','%')
    #print url
    url=urllib2.unquote(url).replace('&amp;','&')
    #delete ''
    url=url[1:-1]
    r=Gzzip.newOpen(url).read()
    pattern=r'italic">(.*?)</a'
    title=re.findall(pattern,r,re.MULTILINE|re.S)
    if len(title)==0:
        title=['no title']
    SQLS="UPDATE `spider` SET `is_named`=1,`title`='"+re.escape(title[0])+"' WHERE `id`="+str(id)+";"
    try:
        print SQLS
        res=cursor.execute(SQLS)
    except Exception:
        pass
    f.write(SQLS)
    #print "采集到",WHERE
    #if WHERE%10==0:

#设置线程数
WORKERS=20
WHERE=0
SQLS=""
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


f=open('tsql.txt','a');
queue = Queue.Queue(0)
#
for i in range(WORKERS):
    Worker(queue).start()
#
for url in imgUrlList:
    queue.put((url[0],url[1]))

#确保队列执行完毕，再执行后面的代码
for i in range(WORKERS):
    queue.put(None)
queue.join()


#关闭数据库连接
f.close()
cursor.close()
conn.close()
print "all done"