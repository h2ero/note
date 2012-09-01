#!/usr/bin/python
#coding=utf8
import shutil,os
#import MySQLdb,time
"""conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')
conn.select_db('weimei');
cursor=conn.cursor()"""
srcDIR='./img/'
fileList=os.listdir(srcDIR)
for i in fileList:
    imgid=i.split('.')[0]
    n=int(i.split('.')[0])%10
    desDIR='%s/'%n
    #sql="UPDATE `spider` SET `isrc`='"+desDIR+i+"' WHERE id="+str(imgid)
    #print sql
    #time.sleep(.01)
    #cursor.execute(sql)
    if os.path.isdir(desDIR):
        shutil.copy(srcDIR+i,desDIR+i)
    else:
        os.mkdir(desDIR)
        print "mkdir,",desDIR
        shutil.move(srcDIR+i,desDIR+i)
"""cursor.close()
conn.close()"""