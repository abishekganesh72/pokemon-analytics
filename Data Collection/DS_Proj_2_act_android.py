# -*- coding: utf-8 -*-
#!/usr/bin/env python

# written By : Abishek Ganesh
#=====================
#http://stackoverflow.com/questions/19591458/python-reading-from-a-file-and-saving-to-utf-8
#import codecs
#with codecs.open(filename,'r',encoding='utf8') as f:
#===================== 

#Sending Email
from send_email import send_email

#DS Project 2

#use Python 3
import sys
import codecs
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import datetime
from datetime import date
from datetime import time
from pprint import pprint
import pandas as pd
import re
import json


#setup data
path = r'../Pokemon/data'
skipped_files_android = []
files_list_android=[]
sep  = '/'
data_android=defaultdict()
counter=0

# find all android ending files
for dirc in os.listdir(path):
	file_dir = '{}{}{}'.format(path, sep, dirc)
	for files in os.listdir(file_dir):
		if '_android' in files: 
			file_path = '{}{}{}'.format(file_dir, sep ,files)
			files_list_android.append(file_path)
print(len(files_list_android))


#read files and extract the data from android files
try: 
	for android_file in files_list_android:
		keyargs = android_file.split(sep)
		date_key = keyargs[-2].split('-')
		time_key = keyargs[-1].split('_')
		key = datetime.datetime(int(date_key[0]), int(date_key[-2]), int(date_key[-1]), int(time_key[0]),int(time_key[1]))
		try:
			with codecs.open(android_file, 'r', encoding='utf-8') as fin:
				soup = BeautifulSoup(fin)
				try:
					android_avg_rating = soup.findAll('div', {'class':"score"})[0].text.strip()
				except:
					android_avg_rating =-9999
				try:
					android_total_ratings = soup.find('span',{'class':'reviews-num'}).text.strip().replace(',', '')
				except:
					android_total_ratings =-9999
				try:
					android_ratings_1 =soup.find('div', {'class':'rating-bar-container one'}).text.strip().split()[-1].replace(',', '').strip()
				except:
					android_ratings_1 =-9999
				try:
					android_ratings_2 =soup.find('div', {'class':'rating-bar-container two'}).text.split()[-1].replace(',', '').strip()
				except:
					android_ratings_2 =-9999
				try:
					android_ratings_3 =soup.find('div', {'class':'rating-bar-container three'}).text.split()[-1].replace(',', '').strip()
				except:
					android_ratings_3 =-9999
				try:
					android_ratings_4 =soup.find('div', {'class':'rating-bar-container four'}).text.split()[-1].replace(',', '').strip()
				except:
					android_ratings_4 =-9999
				try:
					android_ratings_5 =soup.find('div', {'class':'rating-bar-container five'}).text.split()[-1].replace(',', '').strip()
				except:
					android_ratings_ =-9999
				try:
					android_file_size = soup.find('div', {'itemprop':"fileSize"}).text.replace('M', '').strip()
				except:
					android_file_size = -9999
				data_android[key]={'android_avg_rating':float(android_avg_rating),
				      		'android_total_ratings':int(android_total_ratings),
				      		'android_ratings_1':int(android_ratings_1),
				      		'android_ratings_2':int(android_ratings_2),
				      		'android_ratings_3':int(android_ratings_3),
				      		'android_ratings_4':int(android_ratings_4),
				      		'android_ratings_5':int(android_ratings_5),
				      		'android_file_size':int(android_file_size)}
		except Exception as e:
                        data_android[key]={'android_avg_rating':float(android_avg_rating),
				      		'android_total_ratings':0,
				      		'android_ratings_1':0,
				      		'android_ratings_2':0,
				      		'android_ratings_3':0,
				      		'android_ratings_4':0,
				      		'android_ratings_5':0,
				      		'android_file_size':0}
                        skipped_files_android.append(android_file)
                        print('Skipped file: {}'.format(android_file))
                        json.dump(skipped_files_android, open('android_skipped_files.json', 'w'), indent=4)
                        print(e)
                        continue
                #save to data frame to save inporgress data
                pd.DataFrame(data_android).transpose().to_csv('inprogress_data_android.csv')
                
                counter+=1
                if(counter%1000.0==0):
                        msg = 'android Files under process'
                        sub = 'android Status update: {}/{}'.format(counter, len(files_list_android))
                        send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , sub, msg)
        df = pd.DataFrame(data_android)
        print(df.transpose().head())
        df.transpose().to_csv('android_processed_data.csv')
        pprint('skipped files {}'.format(skipped_files_android))
        json.dump(skipped_files_android, open('android_skipped_files.json', 'w'), indent=4)
        send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , 'android Job Done', 'android Job Done')
        
	
except Exception as e:
	
	sub = 'Error in <android> Process Check'
	msg = 'Status update: {}/{}: Error Message : {}, trace:{}'.format(counter, len(files_list_android), e, sys.exc_info())                        
	send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , sub, msg)	
	
	print(sys.exc_info())

	print(e)
