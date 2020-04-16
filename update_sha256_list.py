#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1. Open sha256 list file, and get sha256 list
# 3. Check if sha256 is existed in repo

from __future__ import print_function
import os

f_sha256 = "2018.txt"
f_1 = "2.txt"
folder_repo = "../nkrepo/DATA/"
list_sha256 = []
list_sha256_left = []

def main():
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
            #print("[i]: Existed {}".format(s))
            continue
        list_sha256_left.append(s)
        #count = count + 1

    with open(f_1,'w') as f:
        for item in list_sha256_left:
            f.write('{}\n'.format(item))
    
if __name__ == "__main__":
    main()
