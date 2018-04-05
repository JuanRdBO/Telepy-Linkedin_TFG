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


# define parser
parser = OptionParser()
# Input argumento
#parser.add_argument('Company to be searched', nargs='+')
usage = "usage: %prog [options] Company to be searched"
parser = OptionParser(usage=usage)
parser.add_option("-f","--file", action="store_true",dest="SAVETOFILE",help="write report to a file, with name of the searched company")
parser.add_option("-e","--export", action="store_true",dest="EXPORTCSV",help="export .json file to a .csv readable one. (only with -f flag)")
parser.add_option("-a","--args", action="store_true",dest="ARGUMENTS",help="open a webbrowser to show relevant search arguments.")
parser.add_option("-i","--install", action="store_true",dest="INSTALL",help="execute to install all dependencies")
parser.add_option("-l","--location", action="store_true",dest="LOCATION",help="to search by location. Search by name is default")
parser.add_option("-s","--start", action="store_true",dest="START",help="to return the result from the point specified by the user")
parser.add_option("-c","--complete", action="store_true",dest="COMPLETE",help="return complete dataset from selection. (only with -f flag)")


# if len(sys.argv)==1:
#     parser.print_help(sys.stderr)
#     sys.exit(1)

# ejecuta función de input
(options, args) = parser.parse_args()

# Se define el access token
application = linkedin.LinkedInApplication(token='AQV48ylIhFTFtAazTsszjj6wIpx1c0B004m5hleCSaqlWPUxEXe7QVLxtzvUNnl_aAsX27ABK4j1uXLxcLnmb4M179xH06nSpDy7Eeahg9gdWLrhzjgB2sY2fQ4mU0Nk1Rs5KQ3FAaifqju9ry08WoCZk04sQ181WqsLXPm5JvHL0TY20THdvQff4KGA_GZznN-uyNNOlqDwMZ1HBm6UkuKARGN1CtjBaHuGgeVK0D2F2P38gjwG0KH_RO5uXFp_4sWFWggtNptY1zXHb1vHcFOOBSTQG_EjN58bjiHVPeMPYRuE1AyiWsFCqBxhKCMR-qCs40iH7hkBYeyXAv8gk7VFrR93aA')



if options.ARGUMENTS==True:
	webbrowser.open('https://developer.linkedin.com/docs/fields/company-profile', new=2)
	print("Showing possible search arguments and quitting.")
	quit()

if options.INSTALL==True:
	os.system("sudo python setup.py install")
	quit()
	

# función de printeo de empresa
def printCompanyInfo(company, starting_point, all_info):
	# Se ejecuta el script de linkedin provisto en el repositorio con search company
	if options.LOCATION==True:
		print_json = application.search_company(selectors=[{'companies': ['name', 'website-url','employee-count-range']}], params={'facet': 'location,'+company, 'start': starting_point})
	else: 
		print_json = application.search_company(selectors=[{'companies': ['name', 'website-url','employee-count-range']}], params={'keywords': company, 'start': starting_point})


	if options.SAVETOFILE==True:

		if not os.path.exists(os.path.dirname("output/json/"+company)):
			    try:
			        os.makedirs(os.path.dirname("output/json/"+company))
			    except OSError as exc: # Guard against race condition
			        if exc.errno != errno.EEXIST:
			            raise
		if all_info==1:
			with open("output/json/"+company+".json", 'a') as f:
				print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
		else:
			# Se guarda en un fichero y se formatea
			with open("output/json/"+company+".json", 'w') as f:
				print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)



	# Se envia a stdout para usuario.
	print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')))

starting_point=0
if options.START==True:
	starting_point = args[1]
#print(starting_point)
# se llama a la función con el primer argumento de la función

counter = 0
all_info = 0

if options.COMPLETE==True:
	
	company_input = ''.join(args[0])
	for index in range(0,3):

		if counter ==1:
			printCompanyInfo(''.join(args[0]), starting_point, all_info)
		else:
			all_info = 1
			printCompanyInfo(company_input, starting_point, all_info)
		
		starting_point = starting_point + 20
		counter = counter +1
		print("Done round number: " + str(counter))

else:
	printCompanyInfo(''.join(args[0]), starting_point,all_info)


if options.EXPORTCSV==True:
	lines = []
	company = ''.join(args[0])
	print(company)
	with open("output/json/"+company+".json", 'r') as f:
	    lines = f.readlines()
	    lines = lines[:-1]

	# if all_info==1:
	# 	with open("output/json/"+company+".json", 'a') as f:
	# 	    f.writelines(lines[:1] + lines[5:]) # This will skip the second line
	# else:
	# Se guarda en un fichero y se formatea
	with open("output/json/"+company+".json", 'w') as f:
		f.writelines(lines[:1] + lines[5:]) # This will skip the second line

	with open("output/json/"+company+".json") as fi:
	    data = json.load(fi)
	    df = pd.DataFrame(data=data['values'])
	    #print(df)

	if not os.path.exists(os.path.dirname("output/csv/")):
	    try:
	        os.makedirs(os.path.dirname("output/csv/"))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	df.to_csv("output/csv/"+company+".csv", index=False)


# ¿Otra query?
# while True: 
# 	var = input("Do you want to search for a company? [y/n] ")
# 	if str(var)=="y":
# 		var_2 = input("Which company? ")
# 		printCompanyInfo(str(var_2))
# 		continue
# 	else:
# 		print("Exiting")
# 		quit()
		

