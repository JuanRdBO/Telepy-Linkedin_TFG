import os
import sys

if int(sys.argv[2]) == 1:
	open = "cat "
else:
	open = "open "

os.system(open+'output/csv/'+sys.argv[1]+'.csv')