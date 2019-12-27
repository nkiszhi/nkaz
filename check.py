#!/usr/bin/python

import sqlite3
import json
import urllib
import glob
import hashlib
import os
import subprocess
from time import sleep
import shutil

file_done = "done.txt"
file_todo = "todo.txt"
file_error = "error.txt"
path_target = "/data/wz"
path_usb_drive = "/Volumes/wz"
path_data = "/data/malware/collection"

def check_todo_duplicated():
  list_todo = []
  list_duplicated = []
  with open(file_todo, 'rb') as f:
    for line in f:
      url = line[:-1]
      #print url
      if url in list_todo:
        list_duplicated.append(url)
        print "Duplicated url: {0}".format(url) 
      else:
        list_todo.append(url)

def remove_error_apk(p=path_usb_drive):
  with open(file_error, 'rb') as f:
    for line in f:
      sha256 = line[:-1]
      if len(sha256) > 64:
        #print sha256
        continue
      d = "{0}/{1}/{2}/{3}/{4}".format(p,sha256[0], sha256[1], sha256[2], sha256)
      #print d
      if os.path.isfile(d):
        print "Delete {0}".format(d)
        os.remove(d)
      else:
        print "Already deleted: {0}".format(d)

def check_done_duplicated():
  with open(file_done, 'rb') as f:
    for line in f:
      apk = line[:-1]
      #if len(apk) > 79: # For server3 "/data/wz/0/0/0/sha256"
      if len(apk) > 152: # For "download?apikey=xxx&sha256=xxx"
        print apk
        #print len(apk)
        if os.path.isfile(apk):
          print "Delete {0}".format(apk)
          os.remove(apk)
        else:
          print "Already deleted: {0}".format(apk)
      
def check_sha256(p=path_target):
  """ update done list in the done.txt """
  list_error = [] # list of error sha256

  # Get all downloaded sha256
  str_list = '0123456789abcdef'
  l = 0
  for i in str_list:
    for j in str_list:
      for k in str_list:
        #print "{0}--{1}--{2}".format(i,j,k)
        d = "{0}/{1}/{2}/{3}/{4}".format(p,i,j,k,"*")
        #print d
        for f in glob.glob(d):
          l = l + 1
          #print f
          f_sha256 = f[15:]
          print f_sha256
          with open(f, 'rb') as f:
            contents = f.read()
          c_sha256 = hashlib.sha256(contents).hexdigest()
          print c_sha256
          if f_sha256 == c_sha256:
            continue
          list_error.append(f_sha256)

  # Save list_error to error.txt
  with open(file_error, "wb") as f:
    for sha256 in list_error:
      sha256 = "{0}\n".format(sha256)
      f.write(sha256)

def check_exist(p=path_data, file_sha256 = "1.txt"):
  i = 0 # number of new samples
  list_new = []
  with open(file_sha256, 'rb') as f:
    for line in f:
      sha256 = line[:-1]
      sample = "{0}/{1}/{2}/{3}/{4}".format(p,sha256[0],sha256[1],sha256[2],sha256)
      if os.path.exists(sample):
        continue
      list_new.append(sha256)
      i += 1
  print " {0} new samples".format(i)
 
  with open(file_sha256, "wb") as f:
    for sha256 in list_new:
      sha256 = "{0}\n".format(sha256)
      f.write(sha256)

if __name__ == "__main__":
  #check_todo_duplicated()
  #check_done_duplicated()
  #remove_error_apk()
  check_exist()
