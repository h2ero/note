#!/usr/bin/python
#coding=utf-8
import threading,re,os
#multithread
import Queue
import Gzzip
import time
import MySQLdb  
#end
def listhref(id):
    url="http://www.imgspark.com/image/popular/all/alltime/"+str(id)+"/"
    r=Gzzip.newOpen(url)
    pattern=r'<div class="image_wrap">\s+<a href="(.*?)"(?:.*?)\s+</div>'
    listHrefs=re.findall(pattern,r,re.MULTILINE|re.S)
    return listHrefs 
def pageContent(url):
	r=Gzzip.newOpen("http://www.imgspark.com"+url)
	src=[]
	#src
	pattern=r'id="lrg_image" src="(.*?)"'
	src.append(re.findall(pattern,r,re.MULTILINE|re.S)[0])
	#location
	pattern=r'<span id="source_content"><a href="(.*?)"'
	try:
		src.append(re.findall(pattern,r,re.MULTILINE|re.S)[0])
	except Exception:
            if len(src)==1:
                 src.append('None')
	#tags
	pattern=r'<ul class="list_tags_horizontal">(.*?)</ul>'
	res=re.findall(pattern,r,re.MULTILINE|re.S)
	pattern=r'title="(.*?)"'
	tags=re.findall(pattern,res[0],re.MULTILINE|re.S)
	src.append(tags)
	return src
#print pageContent("http://www.imgspark.com/image/view/5033cf88eb1bb2eb66000000/");
def insertSql(img):
    global WHERE
    global SQLS
    WHERE+=1
    print WHERE,"条记录以入库"
    url=img[0]
    location=img[1]
    #if 2<=len(img[2]):
    tag=','.join(img[2])
    #else:
    #tag=img[2]
    sql="INSERT INTO `pic`(`url`,`location`,`tag`) VALUES('%s','%s','%s');" % (url,re.escape(location),re.escape(tag))
    SQLS+=sql
    if WHERE%50==0:
        f.write(SQLS);
        SQLS=""

    """sql=sql.decode('utf8','ignore');
    try:
        cursor.execute(sql)
    except Exception, e:
        pass"""

#multithread

WORKERS =100
WHERE=0
SQLS=""
#奇怪的问题，WHERE不能发到RUN中，否则最后的时间不能输出
class Worker(threading.Thread):
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            item = self.__queue.get()
            #if item==None:
            #    break
            insertSql(pageContent(item))
            self.__queue.task_done()


#
# try it
#mysql
"""conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')  
conn.select_db('spider');
cursor=conn.cursor()"""
f=open('sql.txt','a');
queue = Queue.Queue(0)

startTime=time.time()
os.environ['TZ'] = 'Hong_Kong'
for i in range(WORKERS):
    Worker(queue).start() # start a worker
for i in range(2):
	li=listhref(i)
	for x in li:
	    queue.put(x)
#确保队列执行完毕，再执行后面的代码
#for i in range(WORKERS):
#    queue.put(None)
queue.join()
#for i in range(WORKERS):
    #queue.put(None) # add end-of-queue markers
#conn.commit()
"""cursor.close()
conn.close()"""
f.close()
endTime=time.time()
print "共耗时:",time.strftime('%H:%M:%S',time.strptime(time.ctime((endTime-startTime))))