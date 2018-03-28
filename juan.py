from linkedin import linkedin
import json

# Se define el access token
application = linkedin.LinkedInApplication(token='AQV48ylIhFTFtAazTsszjj6wIpx1c0B004m5hleCSaqlWPUxEXe7QVLxtzvUNnl_aAsX27ABK4j1uXLxcLnmb4M179xH06nSpDy7Eeahg9gdWLrhzjgB2sY2fQ4mU0Nk1Rs5KQ3FAaifqju9ry08WoCZk04sQ181WqsLXPm5JvHL0TY20THdvQff4KGA_GZznN-uyNNOlqDwMZ1HBm6UkuKARGN1CtjBaHuGgeVK0D2F2P38gjwG0KH_RO5uXFp_4sWFWggtNptY1zXHb1vHcFOOBSTQG_EjN58bjiHVPeMPYRuE1AyiWsFCqBxhKCMR-qCs40iH7hkBYeyXAv8gk7VFrR93aA')


# Se ejecuta el script de linkedin provisto en el reositorio con search company
print_json = application.search_company(selectors=[{'companies': ['name', 'universal-name', 'website-url']}], params={'keywords': 'Telefónica'})

# Se formatea el output 
print(json.dumps(print_json, sort_keys=True,indent=4, separators=(',', ': ')))

