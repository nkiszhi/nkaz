import pandas as pd

list_sha256_all = []
list_sha256_2019_left = []
list_sha256_2018_left = []
list_sha256_2017_left = []

f_sha256_all = '../nkrepo/sha256.txt'
f_sha256_2019_left = 'sha256_2019_left.txt'
f_sha256_2018_left = 'sha256_2018_left.txt'
f_sha256_2017_left = 'sha256_2017_left.txt'

with open(f_sha256_all,'r') as f:
    for line in f:
        list_sha256_all.append(line.strip('\n'))
        print("ALL: {} samples".format(len(list_sha256_all)))

with open(f_sha256_2019_left, 'r') as f:
    for line in f:
        list_sha256_2019_left.append(line.strip('\n'))
        print("2019: {} samples left".format(len(list_sha256_2019_left)))

with open(f_sha256_2018_left, 'r') as f:
    for line in f:
        list_sha256_2018_left.append(line.strip('\n'))
        print("2018: {} samples left".format(len(list_sha256_2018_left)))

with open(f_sha256_2017_left, 'r') as f:
    for line in f:
        list_sha256_2017_left.append(line.strip('\n'))
        print("2017: {} samples left".format(len(list_sha256_2017_left)))

list_sha256_2019_left = list(set(list_sha256_2019_left) - set(list_sha256_all))
list_sha256_2018_left = list(set(list_sha256_2018_left) - set(list_sha256_all))
list_sha256_2017_left = list(set(list_sha256_2017_left) - set(list_sha256_all))

print("2019: {} samples left".format(len(list_sha256_2019_left)))
print("2018: {} samples left".format(len(list_sha256_2018_left)))
print("2017: {} samples left".format(len(list_sha256_2017_left)))

with open(f_sha256_2019_left,'w') as f:
    for item in list_sha256_2019_left:
        f.write('{}\n'.format(item))

with open(f_sha256_2018_left,'w') as f:
    for item in list_sha256_2018_left:
        f.write('{}\n'.format(item))

with open(f_sha256_2017_left,'w') as f:
    for item in list_sha256_2017_left:
        f.write('{}\n'.format(item))



