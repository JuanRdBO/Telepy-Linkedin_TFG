#!/usr/bin/env python
# -*- coding: utf-8 -*-

from linkedin import linkedin
import sys
import argparse
import json
from optparse import OptionParser
import os
import errno
import pandas as pd
import webbrowser
import csv
from pathlib import Path
import glob
import io
import codecs
import re

from renew_token.access_token import ACCESS_TOKEN

parser = OptionParser()
(options, args) = parser.parse_args()


#print(args)




class TELEPY:
	# def __init__(self, token):
	# 	self.token = token
		# Se define el access token para Telepy_2
		

	def retrieve_json(self,token,company, starting_point, count, query_type):

		token_juan = ACCESS_TOKEN(token)
		token_juan.read_csv(token)
		#print('Access Token: '+token_juan.read_csv(token)+'\n\n')
		self.application = linkedin.LinkedInApplication(token=token_juan.read_csv(token))

		if query_type == "by_location":
			print_json = self.application.search_company(selectors=[{'companies': ['id','name','email-domains','company-type','website-url','industries','status','twitter-id','employee-count-range','locations:(is-headquarters,is-active,address,contact-info)','founded-year','end-year','num-followers','specialties']}], params={'facet': 'location,'+company, 'start': starting_point, 'count': count})
		elif query_type == "by_name": 
			print_json = self.application.search_company(selectors=[{'companies': ['id','name','email-domains','company-type','website-url','industries','status','twitter-id','employee-count-range','locations:(is-headquarters,is-active,address,contact-info)','founded-year','end-year','num-followers','specialties']}], params={'keywords': company, 'start': starting_point, 'count': count})
			
		return json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': '))

	def save_to_json(self, name, json_text):

		if not os.path.exists(os.path.dirname("output/json/"+name)):
			try:
			    os.makedirs(os.path.dirname("output/json/"+name))
			except OSError as exc: # Guard against race condition
			    if exc.errno != errno.EEXIST:
			        raise
		
		with open("output/json/"+name, 'w') as f:
			f.write(json_text)
			f.close()

	def convert_to_csv(self):

		if not os.path.exists(os.path.dirname("output/csv/")):
		    try:
		        os.makedirs(os.path.dirname("output/csv/"))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise
		json_files = os.listdir("output/json/")
		json_files.sort()
		print(json_files)
		sub = ".json"
		
		for filename in json_files:
		    if sub in filename:
		        filename = filename[:-5]
		        print("\nConverting '"+filename+ "' to CSV")
		        command = "python -m libjson2csv.json_2_csv './output/json/"+filename+".json' './output/csv/"+filename+".csv'"
		        os.system(command)
	def atof(self,text):
	    try:
	        retval = float(text)
	    except ValueError:
	        retval = text
	    return retval

	def natural_keys(self,text):
	    '''
	    alist.sort(key=natural_keys) sorts in human order
	    http://nedbatchelder.com/blog/200712/human_sorting.html
	    (See Toothy's implementation in the comments)
	    float regex comes from https://stackoverflow.com/a/12643073/190597
	    '''
	    return [ self.atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]


	def unify_all_csv(self):

		if not os.path.exists(os.path.dirname("output/csv/final_company.csv")):
		    try:
		        os.makedirs(os.path.dirname("output/csv/final_company.csv"))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

		csv_files = os.listdir("output/csv/")
		csv_files.sort(key=self.natural_keys)
		print(csv_files)
		sub = ".csv"

		print("\n---------------------------------\n\nUnifying now all CSV files into a big one\n")

		for filename in csv_files:
			
			if sub in filename:
				if not Path("output/csv/final_company.csv").is_file():
					company_csv = pd.read_csv("output/csv/"+filename, dtype='unicode')
					company_csv.to_csv("output/csv/final_company.csv", index=False)
				else:
					company_csv = pd.read_csv("output/csv/final_company.csv", dtype='unicode')
					pandas_csv = pd.read_csv("output/csv/"+filename, dtype='unicode')
					concat_csv = [company_csv, pandas_csv]
					final_company = pd.concat(concat_csv)
					final_company.to_csv("output/csv/final_company.csv", index=False)
			print("Unified file " + filename , end="\r")

		print("\nFinished unifying all csv files to: 'final_company.csv'")




TELEPY = TELEPY()

company = 'ar:0'
starting_point = 0
iterations = 10#50275
app = 100

for index in range(0,iterations):
	while(True):
		try:
			

			new_search = TELEPY.retrieve_json(app, company, starting_point, 1, 'by_location')

			TELEPY.save_to_json(str(starting_point)+"."+company+'.json', new_search)

			starting_point+=1

			print("Processed " + str(starting_point) + " of " + str(iterations) + " JSON files", end="\r")
		except Exception as e:
			app = app + 1
			print(e)
			print("\n--------------------\n\nTrying app " + str(app)+": \n")
			if app == 250:
				print('\n\n--> No more apps from which to source of. Aborting.')
				quit()
			continue
		break 

TELEPY.convert_to_csv()

TELEPY.unify_all_csv()

