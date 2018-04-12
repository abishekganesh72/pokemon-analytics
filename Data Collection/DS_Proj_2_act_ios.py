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
skipped_files_ios = []
files_list_ios=[]
sep  = '/'
data_ios=defaultdict()
counter=0

# find all ios ending files
for dirc in os.listdir(path):
	file_dir = '{}{}{}'.format(path, sep, dirc)
	for files in os.listdir(file_dir):
		if '_ios' in files: 
			file_path = '{}{}{}'.format(file_dir, sep ,files)
			files_list_ios.append(file_path)


print(len(files_list_ios))


#read files and extract the data from ios files
try: 
	for ios_file in files_list_ios:
		keyargs = ios_file.split(sep)
		date_key = keyargs[-2].split('-')
		time_key = keyargs[-1].split('_')
		key = datetime.datetime(int(date_key[0]), int(date_key[-2]), int(date_key[-1]), int(time_key[0]),int(time_key[1]))
		try:
			with codecs.open(ios_file, 'r', encoding='utf-8') as fin:
				soup = BeautifulSoup(fin)
				try:
					ios_current_ratings  = soup.findAll('span', {'itemprop':"reviewCount"})[0].text.split()[0].strip()
				except:
					ios_current_ratings  = -9999
				try:
					ios_all_ratings =  soup.findAll('span', {'class':'rating-count'})[1].text.split()[0].strip()
				except:
					ios_all_ratings =  -9999
				try:	
					ios_file_size =soup.findAll('ul', {'class':'list'})[0].findAll('li')[4].text.split(':')[-1].split()[0].strip()
				except:
					ios_file_size =-9999
				data_ios[key]={'ios_current_ratings':int(ios_current_ratings),
                                               'ios_all_ratings':int(ios_all_ratings),
                                               'ios_file_size':int(ios_file_size)}
		except Exception as e:
                        data_ios[key]={'ios_current_ratings':0,
                                        'ios_all_ratings':0,
                                        'ios_file_size':0}
                        skipped_files_ios.append(ios_file)
                        json.dump(skipped_files_ios, open('ios_skipped_files.json', 'w'), indent=4)
                        print('Skipped file: {}'.format(ios_file))
                        print(e)
                        continue
                #save to data frame to save inporgress data
                pd.DataFrame(data_ios).transpose().to_csv('inprogress_data_ios.csv')
                
                counter+=1
                if(counter%1000.0==0):
                        msg = 'iOS Files under process'
                        sub = 'iOS Status update: {}/{}'.format(counter, len(files_list_ios))
                        send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , sub, msg)
        df = pd.DataFrame(data_ios)
        print(df.transpose().head())
        df.transpose().to_csv('ios_processed_data.csv')
        pprint('skipped files {}'.format(skipped_files_ios))
        json.dump(skipped_files_ios, open('ios_skipped_files.json', 'w'), indent=4)
        send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , 'iOS Job Done', 'iOS Job Done')
        
	
except Exception as e:
	
	sub = 'Error in <iOS> Process Check'
	msg = 'Status update: {}/{}: Error Message : {}, trace:{}'.format(counter, len(files_list_ios), e, sys.exc_info())                        
	send_email('sys7i7an0@gmail.com', '####',  '7i7an0@gmail.com' , sub, msg)	
	
	print(sys.exc_info())

	print(e)
