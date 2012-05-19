#! /usr/bin/python
from bs4 import BeautifulSoup
import MySQLdb  
import  urllib
#print urllib.__doc__
#list page
def getlist(url):
    print url
    temp={}
    r=urllib.urlopen(url).read().decode('gb2312','ignore')
    #get link
    li= BeautifulSoup(r).select('div.mlist li')#find_all("div", { "class" : "c_contentcj" })#.find_all('a')
    index=0
    for i in li:
        #movie title and link
        ss=BeautifulSoup(str(i))
        s=ss.select('div.c_contentcj a')#find_all("div", { "class" : "c_contentcj" })#.find_all('a')
        s=BeautifulSoup(str(s))
        temp[index]=s.get_text()
        temp[index+1]=s.a['href']
        #movie class and zone
        z=ss.select('span.t_datecj')
        s=BeautifulSoup(str(z))
        s=s.get_text().replace('[','').replace(']','').split(',')
        temp[index+2]=s[0]
        temp[index+3]=s[1]
        index+=4
    return temp
#content page
def getContent(url):
    temp={}
    r=urllib.urlopen(url).read().decode('gb2312','ignore')
    R=BeautifulSoup(r)
    #get pic 
    img=R.select('div.img  img')#find_all("div", { "class" : "c_contentcj" })#.find_all('a')
    img=BeautifulSoup(str(img))
    temp['src']=img.img['src']
    #get desc pic
    desc=R.select('div.moviecontent img')
    desc=BeautifulSoup(str(desc))
    temp['desc']=desc.img['src']
    #get qvod link
    qvod=R.select('div#playlist1 a')
    qvod=BeautifulSoup(str(qvod))
    temp['qvod']=qvod.get_text()
    return temp
#print getlist('http://hnydfc.net/list/list0_2.html')
#for i in range(1,100):
#mysql
conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')  
cursor = conn.cursor()
conn.select_db('python')  

site="http://955zy.com"
for n in range(2,458):
    url=('http://955zy.com/list/list0_'+str(n)+'.html')
    li=getlist(url)
    print li
    for cli in range(0,li.__len__(),4):
        print (site+li.get(cli+1))
        c=getContent(site+li.get(cli+1))
        c['name']=li.get(cli)
        c['zone']=li.get(cli+2)
        c['class']=li.get(cli+3)
        print c
        cursor.execute("INSERT INTO `python`.`movie` (`id`, `name`, `src`, `descSrc`, `qvod`, `zone`, `class`) VALUES (NULL, %s, %s, %s, %s,%s,%s)",(str(c['name']),c['src'],c['desc'],str(c['qvod']),str(c['zone']),str(c['class'])));
        conn.commit()
cursor.close()
