from linkedin import linkedin
import sys
import argparse
import json
from optparse import OptionParser
import os
import errno



# define parser
parser = OptionParser()
# Input argumento
#parser.add_argument('Company to be searched', nargs='+')
usage = "usage: %prog [options] Company to be searched"
parser = OptionParser(usage=usage)
parser.add_option("-f","--file", action="store_true",dest="SAVETOFILE",help="write report to a file, with name of the searched company")
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
# ejecuta función de input
(options, args) = parser.parse_args()

# Se define el access token
application = linkedin.LinkedInApplication(token='AQV48ylIhFTFtAazTsszjj6wIpx1c0B004m5hleCSaqlWPUxEXe7QVLxtzvUNnl_aAsX27ABK4j1uXLxcLnmb4M179xH06nSpDy7Eeahg9gdWLrhzjgB2sY2fQ4mU0Nk1Rs5KQ3FAaifqju9ry08WoCZk04sQ181WqsLXPm5JvHL0TY20THdvQff4KGA_GZznN-uyNNOlqDwMZ1HBm6UkuKARGN1CtjBaHuGgeVK0D2F2P38gjwG0KH_RO5uXFp_4sWFWggtNptY1zXHb1vHcFOOBSTQG_EjN58bjiHVPeMPYRuE1AyiWsFCqBxhKCMR-qCs40iH7hkBYeyXAv8gk7VFrR93aA')

# función de printeo de empresa
def printCompanyInfo(company):
	# Se ejecuta el script de linkedin provisto en el repositorio con search company
	print_json = application.search_company(selectors=[{'companies': ['name', 'universal-name', 'employee-count-range', 'locations', 'website-url']}], params={'keywords': company})

	if not os.path.exists(os.path.dirname("output/"+company)):
	    try:
	        os.makedirs(os.path.dirname("output/"+company))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	if options.SAVETOFILE==True:
		# Se guarda en un fichero y se formatea
		with open("output/"+company+".txt", 'w') as f:
			print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')),file=f)
	# Se envia a stdout para usuario.
	print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')))
# se llama a la función con el primer argumento de la función
printCompanyInfo(''.join(args))

# ¿Otra query?
while True: 
	var = input("Do you want to search for another company? [y/n] ")
	if str(var)=="y":
		var_2 = input("Which company? ")
		printCompanyInfo(str(var_2))
		continue
	else:
		print("Exiting")
		quit()
		

