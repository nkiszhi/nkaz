#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1. Open sha256 list file, and get sha256 list
# 3. Check if sha256 is existed in repo

from __future__ import print_function
import os
from time import sleep

folder_repo = "../nkrepo/DATA/"

def update(f_sha256, f_left):
    list_sha256 = []
    list_sha256_left = []
    with open(f_sha256, 'r') as f:
        for line in f:
            list_sha256.append(line.strip('\n').lower())
    print("[i]: {} samples in {}".format(len(list_sha256), f_sha256))
   
    count = 0
    for s in list_sha256:
        p = folder_repo + "{}/{}/{}/{}/{}".format(s[0],s[1],s[2],s[3],s)
        #print(s)
        #print(p)
        if os.path.exists(p):
            count = count + 1
            print("{}: Existed {}".format(count, s))
            continue
        list_sha256_left.append(s)
        #count = count + 1

    with open(f_left,'w') as f:
        for item in list_sha256_left:
            f.write('{}\n'.format(item))

def main():
    update("2015.txt", "2015.txt")
    update("2016.txt", "2016.txt")
    update("2017.txt", "2017.txt")
    update("2018.txt", "2018.txt")
    update("2019.txt", "2019.txt")
    update("2020.txt", "2020.txt")
    update("sha256.txt", "sha256.txt")
    
if __name__ == "__main__":
    main()
