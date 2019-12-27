import os

url = 'download?apikey=26086b61d655c9f00f3aa915cc63831ad87acb5a9ea661db921f52bb5f6ea868&sha256='
path = os.listdir('./')

with open('todo.txt','rb') as f:
  temp =f.read().split('\n')
  temp.remove('')

list_todo = []

for i in temp:
  if url + i[-64:] not in path:
    list_todo.append(i)

with open('todo_new.txt','wb') as g:
  for j in list_todo:
    g.write(j + '\n')


os.system('rm -r ' + 'ml*.txt')
os.system('mv todo_new.txt' + ' todo.txt')
