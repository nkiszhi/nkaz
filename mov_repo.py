#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Move downloaded samples by wget into repo """

from __future__ import print_function
import os
import shutil
from time import sleep
import hashlib

# Move samples downloaded by wget into repo
# samples' name are very long
def mov_raw_samples(folder_download, folder_repo):

    files = os.listdir(folder_download)
    if not files:
        return 0
    print("[o]: Moving samples in {}".format(folder_download))
    count = 0
    del_count = 0
    for sample in files:
        if len(sample) != 152:
            continue
        sha256 = sample[88:].lower()
        #print(sample[88:])
        #print(sha256)
        src_path = folder_download + sample
        #print(src_path)
        with open(src_path, "rb") as f:
            bytes = f.read() # read entire file as bytes
            _sha256 = hashlib.sha256(bytes).hexdigest();
            #print(_sha256)
        if sha256 != _sha256:
            #os.remove(sample)
            continue
        dst_path = folder_repo + "{}/{}/{}/{}/{}".format(sha256[0],sha256[1],sha256[2],sha256[3],sha256)
        if os.path.exists(dst_path):
            os.remove(dst_path)
            del_count = del_count + 1
        shutil.move(src_path, dst_path)
        count = count + 1
        print("[i]: {}  {}".format(count, sha256))
        print("[i]: {}  {}".format(count, _sha256))
        print(" ")

    print("Del {} existed samples ".format(del_count))
    print("Move {} samples ".format(count))
    


def main():
    while 1:
        mov_raw_samples("./data/", "../nkrepo/DATA/")
        sleep(3600)

if __name__ == "__main__":
    main()
