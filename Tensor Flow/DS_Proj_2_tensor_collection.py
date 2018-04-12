# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
#=====================
#http://stackoverflow.com/questions/19591458/python-reading-from-a-file-and-saving-to-utf-8
#import codecs
#with codecs.open(filename,'r',encoding='utf8') as f:
#===================== 
#C:\Users\Abishek\AppData\Local\Programs\Python\Python35\python.exe


#DS Project 2 Tensor Flow Data Collection

#use Python 3

import os
from bs4 import BeautifulSoup
from pprint import pprint
import urllib
sep = '/'
path = r'Pokemon/data'
import json


files_ios=[]
files_android=[]
for dirs in os.listdir(path):
    subdirpath = '{}{}{}'.format(path,sep, dirs )
    for subdir in os.listdir(subdirpath):
        finaldir= '{}{}{}'.format(subdirpath,sep,subdir)
        if 'ios' in finaldir:
            files_ios.append(finaldir)
        if 'android' in finaldir:
            files_android.append(finaldir)
print(len(files_ios), len(files_android))
ios_screenshot_files_list=[]
ios_act_loc=[]
for infile in files_ios:
    soup = BeautifulSoup(open(infile), 'html.parser')
    ios_screenshot_files_list.extend(soup.findAll('img', {'class':'portrait'}))
    for val in soup.findAll('img', {'class':'portrait'}):
        ios_act_loc.append(val.get('src'))
    json.dump(ios_act_loc,open('ios_Screen_progress.json','w'))

final_ios_screens = list(set(ios_act_loc))
print(len(final_ios_screens))
json.dump(final_ios_screens,open('ios_Screen.json','w'))


android_screenshot_files_list=[]
android_act_loc=[]
for infile in files_android[:2]:
    soup = BeautifulSoup(open(infile), 'html.parser')
    android_screenshot_files_list.extend(soup.findAll('img', {'class':'screenshot'}))
    for val in soup.findAll('img', {'class':'screenshot'}):
        android_act_loc.append(val.get('src'))
    json.dump(android_act_loc,open('android_Screen_progress.json','w'))
final_android_screen = list(set(android_act_loc)) 
print(len(final_android_screen))
json.dump(final_android_screen,open('android_Screen.json','w'))


cnt=0
for screen in final_ios_screens:
    cnt+=1
    file_name = screen
    saveloc= 'Pokemon/iosscreen{}.jpeg'.format(cnt)
    urllib.urlretrieve(file_name, saveloc)
    print(screen)

cnt=0
for screen in final_android_screen:
    cnt+=1
    file_name = 'http:{}'.format(screen)
    saveloc= 'Pokemon/androidscreen{}.jpeg'.format(cnt)
    urllib.urlretrieve(file_name, saveloc)
    print(screen)
