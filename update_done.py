#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob 

file_done = "done.txt"
path_data = "/data/malware/collection"

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

if __name__ == "__main__":
  update_done()
