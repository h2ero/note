#!/usr/bin/python
#coding=utf8
from PIL import Image
import os,time
imdir='./img/09/'
lists=os.listdir(imdir)
lists.sort()
for i in lists:
	if len(i.split('.'))==2 and not os.path.exists(imdir+i+".min."+i.split('.')[-1]):
		print "resize",i
		time.sleep(.01)
		im = Image.open(imdir+i)
		left = 0
		top = 0
		width =120
		height = 89
		#保存图片按照宽度270,高度忽略
		size=270,1000000
		im.thumbnail(size, Image.ANTIALIAS)
		im.save(imdir+i+".min."+i.split('.')[-1])
		#图片按照宽度120,高度忽略
		size=120,1000000
		im.thumbnail(size, Image.ANTIALIAS)
		box = (left, top, left+width, top+height)
		#保存到area中
		area = im.crop(box)
		area.save(imdir+i+".mini."+i.split('.')[-1])
	else:
		print i,"skip"