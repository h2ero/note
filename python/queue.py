#! /usr/bin/python
#coding=utf-8
"""
import threading
import time

print time.__doc__;
i=time.time();
i2=time.strptime(time.ctime(i));
print i2.tm_year;

print threading.__all__;
print dir(threading.Thread)#.__all__;
print time.time();
"""

import threading
import Queue
import time, random

WORKERS = 50
class Worker(threading.Thread):

    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                print 'xxxx';
               	break # reached end of queue
            #if self.__queue.qsize==0:
                #print '----------xxxxxxxxxxx-------'
            # pretend we're doing something that takes 10-100 ms
            time.sleep(random.randint(1,1000)/500)
            print "task", item, "finished"
            self.__queue.task_done()

#
# try it

queue = Queue.Queue(20)

for i in range(WORKERS):
    Worker(queue).start() # start a worker

for i in range(200):
    queue.put(i)
print '----------xxxxxxxxxxx-------'
