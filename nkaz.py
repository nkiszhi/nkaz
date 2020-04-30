#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Download android samples from Androzoo.com."""


from __future__ import print_function
import argparse
import os
import multiprocessing
import subprocess
from time import sleep

apikey = r'0d8564dc5820037584f50737244c3ccd296834568a389402d9427278274c1622'
url = 'https://androzoo.uni.lu/api/download?apikey={}&sha256={}'

def worker(dir_result, file_task):
  ''' wget downloads urls in a txt '''
  str_cmd = "wget -P {0} -i {1}".format(dir_result, file_task)
  # -P, --directory-prefix: Set directory to save download files.
  # -i, --input-file: Read URLs from a specified file.
  subprocess.call(str_cmd, shell=True)
  # shell=True: pass args as a string rather than a sequence

def download(n, list_url, dir_result):
  list_workers = []
  print("[o] {} android samples are downloading".format(len(list_url)))
  sleep(5)
  span = len(list_url)/n
  for i in range(n):
    list_tmp = list_url[i*span:(i+1)*span]
    file_task = "task_{0}.txt".format(i+1)
    with open(file_task, "wb") as f:
      for url in list_tmp:
        f.write("{}\n".format(url))
    p = multiprocessing.Process(target=worker, args=(dir_result, file_task,))
    #p.daemon = True
    list_workers.append(p)
    p.start()
  return list_workers

def main():
    file_sha256 = "sha256.txt"
    dir_results = "./data"
    parser = argparse.ArgumentParser(prog="nkaz", description="Download android samples from Androzoo.com")
    parser.add_argument("-s", "--sha256", default=file_sha256, help="Specify a file containing sha256 of Androzoo samples.", type=argparse.FileType('r'))
    parser.add_argument("-r", "--results", default=dir_results, help="Specify a folder to store downloaded samples.")
    args = parser.parse_args()

    list_sha256 = [line.rstrip('\n') for line in args.sha256]
    list_url = [url.format(apikey, x) for x in list_sha256]
    dir_result = args.results
    download(50, list_url, dir_result)

if __name__ == "__main__":
    main()
