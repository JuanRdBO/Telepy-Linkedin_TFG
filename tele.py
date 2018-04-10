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

DEBUG = True

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
parser.add_option("-r","--recursive", action="store_true",dest="RECURSIVE",help="sets how many recursions to be done on 'all data' option. Always 2rd argument. (only with -c flag)")
parser.add_option("-n","--number", action="store_true",dest="NUMBER",help="sets how many companies to be returned. Always 3rd argument. (does not work with -c flag)")
#parser.add_option("-d","--debug", action="store_true",dest="DEBUG",help="sets how many companies to be returned. Always 3rd argument. (does not work with -c flag)")
# if len(sys.argv)==1:
#     parser.print_help(sys.stderr)
#     sys.exit(1)

# ejecuta función de input
(options, args) = parser.parse_args()

# Se define el access token para Telepy
#application = linkedin.LinkedInApplication(token='AQWfQl1JrdtLTLhEXGQI3DnNte281j2pHJWmNg8D54Nz7KaTOKPEHFxt_g6ocKSKq9ef4vRFs5yPOtcrmWSxM1DPHDu3j9GH5YOTLH3xkKxOT-srbWujtFLFyCmKbpKUu-1VxBpOG9x3RIydWt-REqIwsPs3SM6hn_aXbxaVqMw4Nzj9VYBo15nYjPsXts--eLlBQpXJ7rMSY-B4WdFiN9NpWBF3up4UCbnNkbk4F1bAVr5d4OjX_Xbgg2NKnBtL_nuP2t_NQ1Z-0TgaJJy99nBF_-fiR25Dae0eAwgA2_nAqHevfg89c2uCRcKmwqSUPSPppRFwSW75mjRHcW08IAHmS_nRWA')


# Se define el access token para Telepy_2
application = linkedin.LinkedInApplication(token='AQVUPB3mM8mRIut0XK5i_XOm1oVAgMvpxx-uJR8zOXAbr9JNJhyzJJKSlqxXyIZCTYYnhQx3Ydg2-jJwpsA5AiRMqu0L50JTBr0ckJgVPo9WPIabhjUaCK9e_NMxZ8wRu4wgBYrHdW2mt4xOZhpgA0zJrN9DBBVw_Qef3c-clzJKCQYfIkgn5dCqUdTVES_848CobzgEeN8mj8OjYEscQGv8iKAaj55EQELsfDvAzTKYXa--ciiCTzS2NbsQnq5H8vb7XeGV3MF4LFs79hUf80bSzuL01u3eLK25rkPi7QU1cMoCl9gwetM3r0Wxc-99I8FcSWv9KCwWi_bAW9EfIZlx8p--mw')



if options.ARGUMENTS==True:
	webbrowser.open('https://developer.linkedin.com/docs/fields/company-profile', new=2)
	print("Showing possible search arguments and quitting.")
	quit()

if options.INSTALL==True:
	os.system("sudo python setup.py install")
	quit()
	

# función de printeo de empresa
def printCompanyInfo(company, starting_point, all_info, current_round, final_round, count):
	# Se ejecuta el script de linkedin provisto en el repositorio con search company
	if options.LOCATION==True:
		print_json = application.search_company(selectors=[{'companies': ['name', 'website-url','employee-count-range','locations','num-followers','specialties']}], params={'facet': 'location,'+company, 'start': starting_point, 'count': count})
	else: 
		print_json = application.search_company(selectors=[{'companies': ['name', 'website-url','employee-count-range']}], params={'keywords': company, 'start': starting_point, 'count': count})


	if options.SAVETOFILE==True:

		if not os.path.exists(os.path.dirname("output/json/"+company)):
			    try:
			        os.makedirs(os.path.dirname("output/json/"+company))
			    except OSError as exc: # Guard against race condition
			        if exc.errno != errno.EEXIST:
			            raise
		if all_info==1:


			if current_round == 0:
				if not os.path.exists(os.path.dirname("output/json/"+company)):
				    try:
				        os.makedirs(os.path.dirname("output/json/"+company))
				    except OSError as exc: # Guard against race condition
				        if exc.errno != errno.EEXIST:
				            raise

				with open("output/json/"+company+".json", 'w') as f:
					print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
					f.close()
				with open("output/json/"+company+".json", 'r') as f:
				    lines = f.readlines()
				    lines = lines[:-3]
				    f.close()
				with open("output/json/"+company+".json", 'w') as f:
					f.writelines(lines[:1] + lines[5:]) # This will skip the second line
					f.close()
				with open("output/json/"+company+".json", 'a') as f:
					f.write(',\n')
					f.close()

				# with open("output/json/"+company+".json", 'rb+') as f:
				# 	f.seek(-1,2)
				# 	f.write(',\n'.encode())
				# 	f.close()
			
			elif current_round != final_round:

				if not os.path.exists(os.path.dirname("output/json/"+company+"_number_"+str(current_round)+".json")):
				    try:
				        os.makedirs(os.path.dirname("output/json/"+company+"_number_"+str(current_round)+".json"))
				    except OSError as exc: # Guard against race condition
				        if exc.errno != errno.EEXIST:
				            raise

				with open("output/json/"+company+"_number_"+str(current_round)+".json", 'w') as f:				
					print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
				f.close()
				with open("output/json/"+company+"_number_"+str(current_round)+".json", 'r') as f:
				    lines = f.readlines()
				    lines = lines[:-3]
				    f.close()
				with open("output/json/"+company+"_number_"+str(current_round)+".json", 'w') as f:
					f.writelines(lines[6:]) # This will skip the second line
					f.close()
				with open("output/json/"+company+"_number_"+str(current_round)+".json", 'a') as f:
					f.write(',\n')
					f.close()    
				
				# with open("output/json/"+company+"_number_"+str(current_round)+".json", 'rb+') as f:
				# 	f.seek(-1,2)
				# 	f.write(',\n'.encode())
				# 	f.close()
				f_start = open("output/json/"+company+".json", 'a')
				f_append = open("output/json/"+company+"_number_"+str(current_round)+".json",'r')
				contents_append = f_append.read()
				f_start.write(contents_append)


			else: #current_round == final_round
				
				if not os.path.exists(os.path.dirname("output/json/"+company)):
				    try:
				        os.makedirs(os.path.dirname("output/json/"+company))
				    except OSError as exc: # Guard against race condition
				        if exc.errno != errno.EEXIST:
				            raise

				with open("output/json/"+company+"final"+".json", 'w') as f:	
					
					if DEBUG == True:
						print('DEBUG: Final round')			
					
					print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
					f.close()
				with open("output/json/"+company+"final"+".json", 'r') as f:
				    lines = f.readlines()
				    lines = lines[:-1]
				    f.close()
				with open("output/json/"+company+"final"+".json", 'w') as f:
					f.writelines(lines[6:]) # This will skip the second line
					f.close()
				f_start = open("output/json/"+company+".json", 'a')
				f_append = open("output/json/"+company+"final"+".json",'r')
				contents_append = f_append.read()
				f_start.write(contents_append)
		else:

			# Se guarda en un fichero y se formatea
			with open("output/json/"+company+".json", 'w') as f:
				print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
				f.close()
			with open("output/json/"+company+".json", 'r') as f:
			    lines = f.readlines()
			    lines = lines[:-1]
			    f.close()
			with open("output/json/"+company+".json", 'w') as f:
				f.writelines(lines[:1] + lines[4:]) # This will skip the second line
				f.close()
			# with open("output/json/"+company+".json") as fi:
			#     data = json.load(fi)
			#     df = pd.DataFrame(data=data['values'])

			



	# Se envia a stdout para usuario.
	print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')))

starting_point=0
if options.START==True:
	if options.COMPLETE==True:
		if len(args) > 2:
			starting_point = int(args[2])
	else:
		starting_point = int(args[1])

count = 20
if options.NUMBER == True:
	if options.COMPLETE==True:
		if len(args) > 3:
			count = int(args[3]) 
	else:
		count = int(args[2])
#print(starting_point)
# se llama a la función con el primer argumento de la función

recursive_rounds = 3
if options.RECURSIVE == True:
	if len(args) > 1:
		recursive_rounds = args[1]



counter = 0
all_info = 0
current_round = 0
final_round = 0

if options.COMPLETE==True:
	
	all_info = 1
	company_input = ''.join(args[0])

	rangeList = range(0,int(recursive_rounds))
	
	for index in rangeList:

		current_round = index
		final_round = rangeList[-1]
		
		if DEBUG == True:
			print('DEBUG: Round '+ str(current_round)+' from '+str(final_round)+ ' starting at '+str(starting_point) + ' returning ' +str(count) + ' hit(s)')

		printCompanyInfo(company_input, starting_point, all_info, current_round, final_round, count)
		
		starting_point = starting_point + count
		counter = counter +1
		#print("Done round number: " + str(counter))

else:
	if DEBUG == True:
			print('DEBUG: Round '+ str(current_round)+' from '+str(final_round)+ ' starting at '+str(starting_point) + ' returning ' +str(count) + ' hit(s)')
	printCompanyInfo(''.join(args[0]), starting_point,all_info, current_round, final_round, count)


if options.EXPORTCSV==True:
	lines = []
	company = ''.join(args[0])
	#print(company)

	with open("output/json/"+company+".json") as fi:
	    data = json.load(fi)
	    df = pd.DataFrame(data=data['values'])
	    #print(df)
	    fi.close()
	if not os.path.exists(os.path.dirname("output/csv/")):
	    try:
	        os.makedirs(os.path.dirname("output/csv/"))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	df.to_csv("output/csv/"+company+".csv", index=False)

#print(recursive_rounds)

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
		

