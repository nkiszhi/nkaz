#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import json
import urllib
import glob
import hashlib
import ctypes
import os
import multiprocessing
from threading import Thread
import subprocess
import datetime
from time import sleep
from core.settings import TMP_FOLDER
from core.settings import DATA_FOLDER
from core.settings import DOWNLOAD_TODO_LIST
from core.settings import CURRENT_DOWNLOADED
from core.settings import get_sha256
from core.settings import get_benign_dir
from core.settings import APK_PATH
import sys

def downloader(path_dl, i):
  ''' wget downloads urls in a txt '''
  str_cmd = "wget -P {0} -i {1}".format(path_dl,i)
  subprocess.call(str_cmd, shell=True)

def download(n=100):
  downloaders = []
  list_url = []
  with open(DOWNLOAD_TODO_LIST, 'rb') as f:
    for line in f:
      list_url.append(line)
  print "Total need to download: {0}".format(len(list_url))
  sleep(5)
  s = 1 + len(list_url)/n
  for i in range(n):
    list_tmp = list_url[i*s:i*s+s-1]
    file_name = DATA_FOLDER + "split_task_{0}.txt".format(i+1)
    with open(file_name, "wb") as f:
      for url in list_tmp:
        f.write(url)
    p = multiprocessing.Process(target=downloader, args=(TMP_FOLDER, file_name,))
    #p.daemon = True
    downloaders.append(p)
    p.start()
  return downloaders

def get_downloaded_list():
  while True:
    paths = os.listdir(TMP_FOLDER)
    for i in paths:
      sha256_list = []
      sha256 = i.split('sha256=')[1].lower() 
      if sha256 == get_sha256(TMP_FOLDER + i):
        shutil.move(TMP_FOLDER + i, APK_PATH + sha256)
        os.system('echo "' + i + '" >> ' + CURRENT_DOWNLOADED)

def main():
  #Python父进程退出后，子进程/线程自动退出的办法
  libc = ctypes.CDLL('libc.so.6')
  libc.prctl(1,15)
  p1 = Thread(target=get_downloaded_list, args=())
  p1.start()
  download()
