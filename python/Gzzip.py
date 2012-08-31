#!/usr/bin/python
#coding=utf-8
import urllib2
import random
from gzip import GzipFile
from StringIO import StringIO
import sqlite3

conn = sqlite3.connect('/home/h2ero/.mozilla/firefox/4b2udtpz.default/cookies.sqlite')
c = conn.cursor()
sql="SELECT name,value FROM moz_cookies where host='.google.com' and path='/'"
c.execute(sql)
cookies=c.fetchall()
COOKIE=''
for i in cookies:
    COOKIE+=i[0]+'='+i[1]+';'
conn.commit()
c.close()

#Gzip support
class ContentEncodingProcessor(urllib2.BaseHandler):
    """A handler to add gzip capabilities to urllib2 requests """
 
  # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("X-Forwarded-For", "220.181.111."+str(random.randint(1,255)))
        #req.add_header("Host","www.google.com")
        #req.add_header("User-agent", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        #req.add_header("Referer", "http://www.google.com/sorry/Captcha?continue=http%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Ddgh%26oe%3Dutf-8%26client%3Dubuntu%26channel%3Dfs%26um%3D1%26hl%3Den%26biw%3D1364%26bih%3D582%26ie%3DUTF-8%26sa%3DN%26tab%3Diw%26ei%3Dix9AUJi2FafZigfE4YGoBA&id=6646846212168749979&captcha=bythol&submit=Submit")
        req.add_header("User-agent", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1")
        global COOKIE
        req.add_header("Cookie",COOKIE)
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
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code) # 'class to add info() and
            resp.msg = old_resp.msg
        return resp
 
# deflate support
import zlib
def deflate(data): # zlib only provides the zlib compress format, not the deflate format;
    try: # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)
#end
#new opener
encoding_support = ContentEncodingProcessor
#googleproxy=urllib2.ProxyHandler(proxies = {'http' : '127.0.0.1:8087'})
opener = urllib2.build_opener( encoding_support,urllib2.HTTPHandler,urllib2.HTTPCookieProcessor())
def newOpen(url):
    res= opener.open(url)
    return res

