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
  update_todo()
