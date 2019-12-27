#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import json
import urllib
import glob
import hashlib
import os
import multiprocessing
import subprocess
import datetime
from time import sleep


file_todo = "todo.txt"
file_log = "log.txt"

def init():
  list_url = []
  i = 0
  for file_txt in glob.glob("mal_list_*.txt"):
    i = i+1
    print "{0}: {1}".format(i, file_txt)
    with open(file_txt, 'rb') as f:
      for line in f:
        list_url.append(line)

  if i == 0:
    print "No mal_list_*.txt files"
    return

  print "Total URLs: {0}".format(len(list_url))

  with open(file_todo, "wb") as f:
    for url in list_url:
      f.write(url)

def downloader(i):
  ''' wget downloads urls in a txt '''
  str_cmd = "wget -i {0}".format(i)
  subprocess.call(str_cmd, shell=True)
  

def download(n=20):
  downloaders = []
  list_url = []
  with open(file_todo, 'rb') as f:
    for line in f:
      list_url.append(line)
  print "Total URLs: {0}".format(len(list_url))
  sleep(5)

  s = 1 + len(list_url)/n
  for i in range(n):
    print i
    list_tmp = list_url[i*s:i*s+s-1]
    file_name = "ml_{0}.txt".format(i+1)
    with open(file_name, "wb") as f:
      for url in list_tmp:
        f.write(url)
    p = multiprocessing.Process(target=downloader, args=(file_name,))
    downloaders.append(p)
    p.start()

if __name__ == "__main__":
  download()
