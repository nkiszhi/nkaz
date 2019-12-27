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

file_todo = "todo.txt"
file_done = "done.txt"
path_usb_drive = "/Volumes/wz"
path_data = "/data/malware/collection"
wz_apikey = r'0d8564dc5820037584f50737244c3ccd296834568a389402d9427278274c1622'
zwj_apikey = r'527405107e220d29dcc813ab6ae0f6180fcf039bf35c4221f69aae91569424eb'
url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s'

def change_apikey(new_apikey):
  ''' Change todo.txt apikeys in the url '''
  list_todo = []
  with open(file_todo, 'rb') as f:
    for line in f:
      print line
      sha256 = line[116:-1]
      list_todo.append(sha256)
  print len(list_todo)
  
  if len(list_todo) == 0:
    print "No urls need changing apikey."
    return

  with open(file_todo, 'wb') as f:
    for sha256 in list_todo:
      url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s\n'%(new_apikey,sha256)
      f.write(url)
 
def move_folder():
  src_path = "/data/down/app/app"
  dst_path = "/data/malware/collection"
  l = 0
  offset = len(src_path) + 5
  str_list = '0123456789abcdef'
  for i in str_list:
    for j in str_list:
      print "{0}--{1}".format(i, j)
      d = "{0}/{1}/{2}/*.apk".format(src_path,i,j)
      list_apk = glob.glob(d)
      if len(list_apk) == 0:
        continue
      for apk in list_apk:
        #print apk
        sha256 = apk[offset:-4]
        #print sha256
        new_apk =  "{0}/{1}/{2}/{3}/{4}".format(dst_path, sha256[0], sha256[1], sha256[2],sha256)
        #print new_apk
        if os.path.exists(new_apk):
          print "Duplicated {0}".format(apk)
          os.remove(apk)
          continue
        try:
          shutil.move(apk, new_apk)
          l = l + 1
          print "{0}: {1}".format(l, sha256)
        except IOError:
          print "IOError" 

def move_file(p=path_usb_drive):
  i = 0
  with open(file_done, 'rb') as f:
    for line in f:
      ##print len(line)
      if len(line) != 69:
        continue
      #print line
      apk = line[:-1]
      #print apk
      if os.path.exists(apk):
        i = i + 1
        sha256 = apk[:-4]
        #print sha256
        new_apk = "{0}/{1}/{2}/{3}/{4}".format(p,sha256[0],sha256[1],sha256[2],sha256)
        #print new_apk
        print "{0}: {1}".format(i, sha256)
        shutil.move(apk, new_apk)

def move_download(p=path_usb_drive):
  i = 0
  offset = len("download?apikey=527405107e220d29dcc813ab6ae0f6180fcf039bf35c4221f69aae91569424eb&sha256=")
  with open(file_done, 'rb') as f:
    for line in f:
      #print len(line)
      #print line
      #print line[65:-1]
      if line[:8] == "download":
        apk = line[:-1]
        if len(apk) > 152:
          continue
        if os.path.exists(apk):
          sha256 = apk[offset:] # offset = 88
          new_apk = "{0}/{1}/{2}/{3}/{4}".format(p,sha256[0],sha256[1],sha256[2],sha256)
          if os.path.exists(new_apk):
            continue
          try:
            shutil.move(apk, new_apk)
            i = i + 1
            print "{0}: {1}".format(i, sha256)
          except IOError:
            print "IOError" 

def move_apk(t=1, p=path_data):
  i = 0
  offset = len("download?apikey=527405107e220d29dcc813ab6ae0f6180fcf039bf35c4221f69aae91569424eb&sha256=")
  list_done = []
  list_apk = glob.glob("download?apikey=*")
  print "Found {0} downloaded samples.".format(len(list_apk))
  #print list_apk[0]
  if len(list_apk) == 0:
    return
  sleep(t)
  for apk in list_apk:
    #print apk
    if apk.endswith(".tmp"):
      continue
    f_sha256 = apk[offset:]
    with open(apk, 'rb') as f:
      contents = f.read()
    c_sha256 = hashlib.sha256(contents).hexdigest()
    #print f_sha256
    #print c_sha256 
    if f_sha256 == c_sha256:
      # Move 
      new_apk = "{0}/{1}/{2}/{3}/{4}".format(p,f_sha256[0],f_sha256[1],f_sha256[2],f_sha256)
      if os.path.exists(new_apk):
        print "Existed {0}".format(f_sha256)
        os.remove(apk)
        continue
      #print new_apk
      i = i + 1
      try:
        shutil.move(apk, new_apk)
        print "{0}: {1}".format(i, f_sha256)
      except IOError:
        print "IOError"
    list_done.append(f_sha256)
  append_done_file(list_done)

def update_db():
  conn = sqlite3.connect('malware.db')
  cur = conn.cursor()
  with open(file_done, 'rb') as f:
    for line in f:
      sha256 = line[:-1]
      cur.execute("UPDATE download SET download = 1 WHERE sha256 = ?", (sha256,))
  conn.commit()
  conn.close()

def append_done_file(list_sha256):
  if len(list_sha256) == 0:
    return
  with open(file_done, "a") as f:
    for sha256 in list_sha256:
      sha256 = "{0}\n".format(sha256)
      f.write(sha256) 

def update_done(p=path_data):
  """ update done list in the done.txt """
  list_done = [] # list of sha256 of downloaded files

  offset = len(p) + 7
  # Get all downloaded sha256
  str_list = '0123456789abcdef'
  l = 0
  for i in str_list:
    for j in str_list:
      for k in str_list:
        print "{0}--{1}--{2}".format(i,j,k)
        d = "{0}/{1}/{2}/{3}/{4}".format(p,i,j,k,"*")
        for f in glob.glob(d):
          l = l + 1
          #print f
          sha256 = f[offset:]
          print "{0}: {1}".format(l, sha256)
          list_done.append(sha256)
  print "Have downloaded {0} samples.".format(len(list_done))

  # Save list_done to done.txt
  with open(file_done, "wb") as f:
    for sha256 in list_done:
      sha256 = "{0}\n".format(sha256)
      f.write(sha256)
  return list_done

def update_todo():
  list_done = []
  with open(file_done, 'rb') as f:
    for line in f:
      sha256 = line[:-1]
      list_done.append(sha256)

  # Update todo.txt
  i = 0
  list_todo = []
  with open(file_todo, 'rb') as f:
    for line in f:
      #print line
      sha256 = line[116:-1]
      #print sha256
      if sha256 in list_done:
        i = i+1
        print "{0}: {1} has been downloaded".format(i, sha256) 
        continue
      list_todo.append(line)

  print "Todo list has {0} urls".format(len(list_todo))
  # update todo.txt
  with open(file_todo, "wb") as f:
    for url in list_todo:
      f.write(url)

if __name__ == "__main__":
  #update_done()
  #update_todo()
  #move_folder()
  while True:
    move_apk()
    update_todo()
    sleep(60)
