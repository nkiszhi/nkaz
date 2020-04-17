#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Move samples from samples folder in  the three-level storing architecture
into the repo in four-level storing architecture.""" 

from __future__ import print_function
import os
import shutil
from time import sleep
import hashlib

#input_folder = "./data/"
input_folder = "./3/"
repo_folder = "../nkrepo/DATA/"

# Move samples downloaded by wget into repo
# samples' name are very long
def mov_raw_samples():
    files = os.listdir(input_folder)
    if not files:
        return 0
    print("[o]: Moving samples in {}".format(input_folder))
    count = 0
    del_count = 0
    for sample in files:
        if len(sample) != 152:
            continue
        sha256 = sample[88:].lower()
        #print(sample[88:])
        #print(sha256)
        src_path = input_folder + sample
        #print(src_path)
        with open(src_path, "rb") as f:
            bytes = f.read() # read entire file as bytes
            _sha256 = hashlib.sha256(bytes).hexdigest();
            #print(_sha256)
        if sha256 != _sha256:
            #os.remove(sample)
            continue
        dst_path = repo_folder + "{}/{}/{}/{}/{}".format(sha256[0],sha256[1],sha256[2],sha256[3],sha256)
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
    

# Move samples in one folder into repo
def mov_samples():
    files = os.listdir(input_folder)
    if not files:
        return 0
    print("[o]: Moving samples in {}".format(input_folder))
    count = 0
    for sample in files:
        sha256 = sample.lower()
        if len(sha256) !=64:
            continue
        #print(sha256)
        src_path = input_folder + sample
        with open(src_path, "rb") as f:
            bytes = f.read() # read entire file as bytes
            _sha256 = hashlib.sha256(bytes).hexdigest();
            #print(_sha256)
        if sha256 != _sha256:
            #os.remove(sample)
            continue
        dst_path = repo_folder+"{}/{}/{}/{}/{}".format(sha256[0],sha256[1],sha256[2],sha256[3],sha256)
        print(src_path)
        print(dst_path)
        if os.path.exists(dst_path):
            os.remove(dst_path)
        shutil.move(sample, dst_path)
        count = count + 1
        print("[i]: {}  {}".format(count, sha256))
        print("[i]: {}  {}".format(count, _sha256))
        print(" ")

# Move sample's data files in one folder into repo
def mov_data():
    files = os.listdir(input_folder)
    if not files:
        return 0
    print("[o]: Moving samples in {}".format(input_folder))
    count = 0
    for sample in files:
        l_s = sample.lower() # l_s lower sample name
        #print("{}".format(len(sample)))
        if len(sample) != 69:
            continue
        #print(sha256)
        src_path = input_folder+sample
        dst_path = repo_folder+"{}/{}/{}/{}/{}".format(l_s[0],l_s[1],l_s[2],l_s[3],l_s)
        #print(src_path)
        #print(dst_path)
        if os.path.exists(dst_path):
            os.remove(dst_path)
        shutil.move(src_path, dst_path)
        count = count + 1
        print("[i]: {}  {}".format(count, sample))
        #print(" ")

def mov_repo():
    hex_string = "0123456789abcdef"
    n_delete = 0
    n_mov = 0
    for i in hex_string:
        for j in hex_string:
            for k in hex_string:
                folder = "./samples/{}/{}/{}/".format(i,j,k)
                if not os.path.exists(folder):
                    continue
                files = os.listdir(folder)
                if not files:
                    continue
                print("[o]: Moving samples in {}".format(folder))
                for f in files:
                    if len(f) != 64:
                        #print(f)
                        continue
                    l = f[3]
                    src_path = folder+f
                    dst_path = "./DATA/{}/{}/{}/{}/{}".format(i,j,k,l,f)
                    #print(src_path)
                    #print(dst_path)
                    if os.path.exists(dst_path):
                        # Delete duplicated samples
                        os.remove(src_path)
                        n_delete = n_delete + 1
                        print("[i]: Deleted duplicated sample {}".format(f))
                    else:
                        shutil.move(src_path, dst_path)
                        n_mov = n_mov + 1
    
    print("[o] {} new samples are added into repo.".format(n_mov))
    print("[i] {} duplicated samples are deleted.".format(n_delete))

def main():
    #mov_raw_data()

    #while 1:
    #    mov_raw_samples()
    #    sleep(3600)
    mov_samples()

if __name__ == "__main__":
    main()
