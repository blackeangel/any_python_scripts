# -*- coding: utf-8 -*-
import os, sys

def clear():
	import subprocess as sp
	if os.name==('ce','nt','dos'):
		sp.call('cls',shell=True)
	elif os.name=='posix':
		sp.call('clear',shell=True)
	else:
		print('\n'*120)

def filedirlist(startdir):
	selectfile=''
	dirlist=[]
	otherlist=[]
	clear()
	for i in sorted(os.listdir(startdir)):
		if os.path.isdir(startdir+os.sep+i):
			dirlist.append((startdir+os.sep+i).replace(os.sep+os.sep,os.sep))
		else:
			otherlist.append((startdir+os.sep+i).replace(os.sep+os.sep,os.sep))
	otherlist.sort()
	dirlist.sort()
	dirlist.extend(otherlist)
	print('Current dir: ' + os.path.dirname(dirlist[0]))
	print('b: back')
	k=0
	for k in range(dirlist.__len__()):
		try:
			lk=os.readlink(dirlist[k])
			if os.path.isdir(lk):
				print('\033[96m' + ' '+ str(k) +': '+ dirlist[k].split(os.sep)[-1:][0] + '\033[00m' + ' -> ' + '\033[93m'+ lk+'\033[00m')
			else: 
				if os.path.islink(lk):
					print('\033[96m' + ' '+ str(k) +': '+ dirlist[k].split(os.sep)[-1:][0] + '\033[00m' + ' -> ' + '\033[96m'+ lk+'\033[00m')
				else:
					print('\033[96m' + ' '+ str(k) +': '+ dirlist[k].split(os.sep)[-1:][0] + '\033[00m' + ' -> ' + lk)
			lk=''
		except:
			if os.path.isdir(dirlist[k]):
				print('\033[93m' + ' ' +str(k)+': '+ dirlist[k].split(os.sep)[-1:][0] + '/' + '\033[00m')
			else:
				print(' '+str(k)+': '+dirlist[k].split(os.sep)[-1:][0])
	print('e: exit')
	b = input()
	if b.isdigit()==False:
		if b=='e':
			clear()
			exit
		elif b == 'b':
			clear()
			filedirlist(os.path.dirname(os.path.dirname(dirlist[0])))
	else:
		try:
			if os.readlink(dirlist[int(b)]).isdir():
				filedirlist(os.readlink(dirlist[int(b)]))
			else:
				selectfile=str(os.readlink(dirlist[int(b)]))
		except:
			if os.path.isdir(dirlist[int(b)]):
				filedirlist(dirlist[int(b)])
			else:
				selectfile=str(dirlist[int(b)])
	return selectfile
lmn=filedirlist('/storage')
print(lmn)