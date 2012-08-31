#!/usr/bin/python
#coding=utf8
from PIL import Image
import os,time
import MySQLdb
conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')  
conn.select_db('weimei');
cursor=conn.cursor()
lists=os.listdir('./img')
lists.sort()
for i in lists:
	time.sleep(.01)
	im = Image.open("./img/"+i)
	w,h=im.size
	height=h*270/w
	print i
	cursor.execute("UPDATE `spider` SET `height`="+str(height)+" WHERE id="+str(i.split('.')[0]))

cursor.close()
conn.close()