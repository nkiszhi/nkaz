#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Nankai University
#Email:1103466626@qq.com
#date:2018.09.01

import datetime
import os
from download import download
from core import get_vt
from multiprocessing import Process
from core.settings import deal_with_tmp
from core.settings import TMP_FOLDER
from core.mail import send_email
from core.settings import VT_FILE
from core.settings import SPLIT_TASK_FILE

import ctypes   
libc = ctypes.CDLL('libc.so.6')    
libc.prctl(1,15)

if __name__ == '__main__':
  #创建存放临时文件的路径/data/tmp/
  os.system('mkdir -p ' + TMP_FOLDER)
  
  #将/data/tmp/目录下的样本check sha256后，把下载成功文件的url写到current_downloaded.txt里面
  #然后将current_downloaded.txt和需要下载的总表todo.txt求差集，把下载过的文件的url从总表中移除
  #并把差集的结果重新命名为todo.txt
  deal_with_tmp()

  #开启样本下载进程, 在进程内部使用将需要下载文件的总表切分为100份，同时创建100个wget子进程下载样本
  p1 = Process(target=download.main, args=())
  p1.start()

  #定期中断再执行,每天11:30自动终止程序，即终止wget进程，然后删除wget未完成的任务列表，再次执行
  #deal_with_tmp()函数，check样本，更新current_downloaded.txt和todo.txt,11:35则重新启动下载进程

  flag = 0
  while 1:
    time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if time_string[11:16] == '11:30' and flag==0:
      flag = 1
      os.system('pkill -f wget')
      if p1.is_alive():
        p1.terminate()
      os.system('rm -f ' + SPLIT_TASK_FILE)
      count_download = deal_with_tmp()

    if time_string[11:16] == '11:35' and flag==1:
      flag = 0
      p1 = Process(target=download.main, args=())
      p1.start()

      #p2 = Process(target=get_vt.main, args=())
      #p2.start()
      #if p2.is_alive():
      #  p2.terminate()
      #count_download = deal_with_tmp()
      # Send Email
      #with open(VT_FILE, 'rb') as h:
      #	count_vt = h.read().split('\n')
      #string = '2017------Daily Mail------' + '\nvt_count:' +  count_vt[0] + '\ndownload: ' + str(count_download)
      #Send the number of extraction.
      #      with open(EXTRACTION_FILE,'rb') as h:
      #	count_extraction = h.read().split('\n')
      #      string = string + '\nextracted:'+str(count_extraction)
      #send_email(string)
      #p2 = Process(target=get_vt.main,args=())
      #p2.start()
