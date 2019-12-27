import os
import shutil

path_mal = './malware/'
path_ben = './goodware/'

path1 = os.listdir('./data/')
path2 = os.listdir('./xml/')

set_d = list(set([i[:64] for i in path1]))
set_x = list(set([i[:64] for i in path2]))

with open('2015_malware.txt','rb') as f1:
  list_m = f1.read().split('\n')
  list_m.remove('')

with open('2015_goodware.txt','rb') as f2:
  list_b = f2.read().split('\n')
  list_b.remove('')

for i in set_d:
  if i in list_m and i in set_x:
    shutil.move('./data/' + i +'.data', path_mal)
    shutil.move('./xml/' + i +'.xml', path_mal)

  if i in list_b and i in set_x:
    shutil.move('./data/' + i +'.data', path_ben)
    shutil.move('./xml/' + i +'.xml', path_ben)

for i in set_x:
  if i in list_m and i in set_d:
    shutil.move('./data/' + i +'.data', path_mal)
    shutil.move('./xml/' + i +'.xml', path_mal)

  if i in list_b and i in set_d:
    shutil.move('./data/' + i +'.data', path_ben)
    shutil.move('./xml/' + i +'.xml', path_ben)
