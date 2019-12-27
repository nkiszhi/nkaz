#!/usr/bin/python

import sqlite3
import json
import urllib
import glob
import hashlib
import os
import multiprocessing
import subprocess

file_proposed = "proposed.json"

apikey = r'0d8564dc5820037584f50737244c3ccd296834568a389402d9427278274c1622'
#apikey = r'527405107e220d29dcc813ab6ae0f6180fcf039bf35c4221f69aae91569424eb'
url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s'
path_usb_drive = "/Volumes/wz"

def init_folder(p = path_usb_drive):
  """ Create three level folders at hard disk """
  str_list = '0123456789abcdef'
  for i in str_list:
    for j in str_list:
      for k in str_list:
        d = "{0}/{1}/{2}/{3}".format(p,i,j,k)
        if os.path.isdir(d):
          continue
        print "Make new folder {0}".format(d)
        os.makedirs(d)

def init_db():
  conn = sqlite3.connect('malware.db')
  cur = conn.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS download
    (sha256    text,
     category  text,
     family    text,
     download  integer)''')
  with open(file_proposed,"r") as f:
    dict_mal =json.load(f, encoding = "utf-8")
    for s, c in dict_mal.items(): # s->SHA256, c->category
      cur.execute("INSERT INTO download VALUES (?, ?, '', 0)", (s, c))
  conn.commit()
  conn.close()

def get_download_list():
  ''' Output a txt file. In this txt file, there are urls which are needed to
be downloaded. 
  '''
  conn = sqlite3.connect('malware.db')
  cur = conn.cursor()
  cur.execute("SELECT sha256 FROM download WHERE download == 0")
  list_todo = cur.fetchall()
  conn.commit()
  conn.close()
  
  #with open("list.txt", "wb") as f:
  #  for i in list_todo:
  #    url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s\n'%(apikey,i[0])
  #    f.write(url)
  len_todo = len(list_todo)
  for i in range(len_todo/10000 + 1):
    print i
    list_tmp = list_todo[i*10000:i*10000+9999]
    file_name = "mal_list_{0}.txt".format(i)
    with open(file_name, "wb") as f:
      for j in list_tmp:
        url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s\n'%(apikey,j[0])
        f.write(url)

def update_db():
  conn = sqlite3.connect('malware.db')
  cur = conn.cursor()
  for file_mal in glob.glob("download?apikey=*"):
    if file_mal.endswith(".tmp"):
      continue
    print file_mal
    #print type(file_mal)
    with open(file_mal, 'rb') as f:
      contents = f.read()
    str_sha256 = hashlib.sha256(contents).hexdigest()
    print str_sha256
    cur.execute("UPDATE download SET download = 1 WHERE sha256 = ?",(str_sha256,))
    os.rename(file_mal, "malware/{0}.apk".format(str_sha256))
  conn.commit()
  conn.close()

def split_list(file_list):
  ''' Split a list to small sublists
  '''
  # 1. Get done list from database
  # list_db, a list in database, each item is a tuple
  # list_done, done list of sha256 strings
  conn = sqlite3.connect('malware.db')
  cur = conn.cursor()
  cur.execute("SELECT sha256 FROM download WHERE download == 1")
  list_db = cur.fetchall()
  conn.commit()
  conn.close()
  list_done = []
  for i in list_db:
    list_done.append(i[0])
  print list_done[:5]
  print len(list_done)

  # 2. Get url list from file
  list_url = []
  with open(file_list, "rb") as f:
    for line in f:
      #print line
      #print line[-65:-1]
      sha256 = line[-65:-1]
      if sha256 in list_done:
        continue
      list_url.append(sha256)
  print len(list_url)
  print list_url[:5]

  # 3. Split to 30 sublists
  for i in range(len(list_url)/250 + 1):
    print i
    list_tmp = list_url[i*250:i*250+249]
    file_name = "ml39_{0}.txt".format(i)
    with open(file_name, "wb") as f:
      for j in list_tmp:
        url = 'https://androzoo.uni.lu/api/download?apikey=%s&sha256=%s\n'%(apikey,j)
        f.write(url)

if __name__ == "__main__":
  init_folder() 
  #get_download_list()
  #update_db()
  #split_list("mal_list_39.txt")
  download()
