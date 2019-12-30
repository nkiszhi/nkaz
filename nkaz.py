#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Download android samples from Androzoo.com."""


from __future__ import print_function
import argparse
import os
import multiprocessing
import subprocess

DOWNLOAD_TODO_LIST = ""
DATA_FOLDER = ""
TMP_FOLDER = ""

def downloader(path_dl, i):
  ''' wget downloads urls in a txt '''
  str_cmd = "wget -P {0} -i {1}".format(path_dl,i)
  # -P, --directory-prefix: Set directory to save download files.
  # -i, --input-file: Read URLs from a specified file.
  subprocess.call(str_cmd, shell=True)
  # shell=True: pass args as a string rather than a sequence

def download(n=100):
  list_downloaders = []
  list_url = []
  with open(DOWNLOAD_TODO_LIST, 'rb') as f:
    for line in f:
      list_url.append(line)
  print("[o] {} android samples are downloading".format(len(list_url)))
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
    list_downloaders.append(p)
    p.start()
  return list_downloaders

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
    parser = argparse.ArgumentParser(prog="nkaz", description="Download android samples from Androzoo.com")
    parser.add_argument("-k", "--keys", help="specify a file containing Androzoo keyes.", type=argparse.FileType('r'))
    parser.add_argument("-s", "--sha256", help="specify a file containing sha256 of Androzoo samples.", type=argparse.FileType('r'))
    args = parser.parse_args()

    list_key = [line.rstrip('\n') for line in args.keys]
    print(len(list_key))

if __name__ == "__main__":
    main()
