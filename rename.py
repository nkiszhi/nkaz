#import pandas as pd
import os

path_apk = './'

os.chdir(path_apk)
path = os.listdir('./')

for i in path:
  if i[:8] == 'download':
    try:
      os.rename(i, i[-64:])
    except Exception, e:
      print str(e) + '--------->' + i

strpath = '0123456789ABCDEF'
list_path = list(strpath)

for i in list_path:
  os.popen('mv ' + i + '* ' + './android/')
