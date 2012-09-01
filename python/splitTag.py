#!/usr/bin/python
#coding=utf-8
import MySQLdb
import re
conn = MySQLdb.connect(host='localhost', user='root',passwd='52486258',charset='utf8')
conn.select_db('weimei');
cursor=conn.cursor()
for i in range(1,1000):
    sql="SELECT tag FROM `spider`  where id="+str(i)
    cursor.execute(sql)
    tags=cursor.fetchall()
    for tag in tags[0][0].split(','):
        tag=tag.encode('utf8')
        tag=re.escape(tag)
        sql="SELECT id FROM `tag`  where name='"+tag+"'"
        cursor.execute(sql)
        tagid=cursor.fetchall()
        if len(tagid)!=0:
            sql="UPDATE `tag` SET targetId=concat(targetId,'p"+str(i+529)+",'),sum=sum+1 where id="+str(tagid[0][0])
            print sql
            cursor.execute(sql)
        else:
            sql="INSERT INTO `tag`(`name`, `targetId`,`sum`) VALUES ('%s','%s,',1)" % (tag,'p'+str(i+529))
            print sql
            cursor.execute(sql)
cursor.close()
conn.close()