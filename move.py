import os
import shutil

path = os.listdir('./android/')

for i in path:
  if i[-4:] == 'data':
    shutil.move('./android/' + i, './data/')
  if i[-3:] == 'xml':
    shutil.move('./android/' + i, './xml/')

    
