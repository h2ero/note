#! /usr/bin/python
#coding=utf-8
import MySQLdb  
import urllib2, threading,re,os,urllib
from Queue import Queue
from gzip import GzipFile
from StringIO import StringIO
import random
import time
#Gzip support
class ContentEncodingProcessor(urllib2.BaseHandler):
  """A handler to add gzip capabilities to urllib2 requests """
 
  # add headers to requests
  def http_request(self, req):
    req.add_header("Accept-Encoding", "gzip, deflate")
    req.add_header("User-agent", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0")
    return req
 
  # decode
  def http_response(self, req, resp):
    old_resp = resp
    # gzip
    if resp.headers.get("content-encoding") == "gzip":
        gz = GzipFile(
                    fileobj=StringIO(resp.read()),
                    mode="r"
                  )
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
        resp.msg = old_resp.msg
    # deflate
    if resp.headers.get("content-encoding") == "deflate":
        gz = StringIO( deflate(resp.read()) )
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
        resp.msg = old_resp.msg
    return resp
 
# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
  try:               # so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)
#end
#new opener
encoding_support = ContentEncodingProcessor
opener = urllib2.build_opener( encoding_support,urllib2.HTTPHandler)
#end
#mutilethreading file
class getKeyWord(threading.Thread):
    def __init__(self,keyword):
        self.keyword=keyword
        self.result=None
        threading.Thread.__init__(self)
    def get_result(self):
        return self.result
    def run(self):
        try:
            self.result=sougou(self.keyword)
        except Exception,e:
            print "%s" % (self.keyword)
            
def initkeyword(keywordList):
    result=[]
    def producer(q,keywordList):
        for keyword in keywordList:
            thread=getKeyWord(keyword);
            thread.start()
            q.put(thread,True)
    def consumer(q,total_key):
        while len(result)<total_key:
            thread=q.get(True)
            thread.join(2)
            for i in thread.get_result():
                if(i!=None and len(i)<30):
                    #print "INSERT INTO `keywords`( `name`) VALUES('%s')"%i;
                    print ("INSERT INTO `keywords`( `name`) VALUES('%s')"%i)
                    cursor.execute("INSERT INTO `keywords`( `name`) VALUES('%s')"%i);
                    conn.commit()
    q=Queue(10)
    prod=threading.Thread(target=producer,args=(q,keywordList))
    cons=threading.Thread(target=consumer,args=(q,len(keywordList)))
    prod.start()
    cons.start()
    prod.join(2)
    cons.join(2)
    return result
#end
#urlencode
def urlencode(word):
    query={'wd':word}
    return urllib.urlencode(query);
#end
#urlencode
def urlencode(w,word):
    query={w:word}
    return urllib.urlencode(query);
#end
def baidu(keyword):
    url='http://www.baidu.com/s?ie=utf8&'+urlencode('wd',keyword)
    res=opener.open(url).read().decode('gb2312','ignore').encode('utf8');
    pattern=r'<a(?:.*?)s?wd=(?:.*?)src=0">(.*?)</a>'
    res=re.findall(pattern,res);
    return res;

def soso(keyword):
    url="http://www.soso.com/q?"+urlencode('w',keyword);
    res=opener.open(url).read().decode('gb2312','ignore').encode('utf8');
    pattern='<div ss_c="search.hint" id="rel">(.*)</div>'
    list=re.findall(pattern,res);
    pattern='<a(?:.*?)>(.*?)</a>'
    list=re.findall(pattern,list[0])
    return list   
def sougou(keyword):
    url="http://www.sogou.com/web?"+urlencode('query',keyword)
    res=opener.open(url).read().decode('gb2312','ignore').encode('utf8');
    print res
    pattern=r'<div class="left">(.*?)</ul>'
    res=re.findall(pattern,res);
    pattern='<a(?:.*?)>(.*?)</a>'
    res=re.findall(pattern,res[0])
    return res
#mysql
conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')  
cursor = conn.cursor()
conn.select_db('python')  
#open file 
"""
f=open('sres.txt')
listk=[]
while True:
    line=f.readline()
    if not line:break
    listk.append(line)
f.close()
i=0
t1=time.time()
while i<len(listk):
	print "用时:%d-%d"%(i,i+35)
	i=i+35
	initkeyword(listk[i:i+35])
	print "用时:%f"%(time.time()-t1)
cursor.close()
print "共用时:%f"%(time.time()-t1)
"""
print sougou('头像')
