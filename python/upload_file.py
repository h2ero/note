#!/usr/bin/env python
# encoding: utf-8
import requests

def upload_file():
    session_id = "ecvd4a0u6jb2c4uuj1bjaknmi7"
    cookies = {'PMSID':'ecvd4a0u6jb2c4uuj1bjaknmi7'}
    files = {'userfile':open('c.txt', 'r')}
    uploadurl = 'http://crm.int.jumeicd.com/CRMUser/upload'
    data = {'PMSID':session_id, '_ajax_':'true'}
    r = requests.post(uploadurl, files=files, data=data, cookies=cookies)
    print r.content

upload_file()
