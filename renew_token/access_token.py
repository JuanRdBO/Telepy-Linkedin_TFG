from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)
import sys
from selenium import webdriver
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy


class ACCESS_TOKEN:
    def __init__(self, app):
        self.app = app
        self.app_access_token = ''

    def read_csv(self,app):
        book = xlrd.open_workbook("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/secrets.xls")
        sh = book.sheet_by_index(0)
        for rx in range(1,sh.nrows):
            if rx == self.app:
                self.app_access_token = sh.row(rx)[2].value
                return self.app_access_token
            else:
                pass

    def register(self):
        CLIENT_ID = ''
        CLIENT_SECRET = ''
        RETURN_URL = 'http://localhost:8080/code/'

        book = xlrd.open_workbook("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/secrets.xls")

        sh = book.sheet_by_index(0)
        for rx in range(1,sh.nrows):
            if rx == self.app:
                CLIENT_ID = sh.row(rx)[0].value
                CLIENT_SECRET =sh.row(rx)[1].value
            else:
                pass

        authentication = LinkedInAuthentication(
                            CLIENT_ID,
                            CLIENT_SECRET,
                            RETURN_URL,
                            permissions=['r_basicprofile']
                        )
        #Authentification URL
        #print('\nAuthentification URL:\n'+authentication.authorization_url)
        application = LinkedInApplication(authentication)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        driver = webdriver.Chrome('/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/chromedriver')
        driver.get(authentication.authorization_url)
        #python_button = driver.find_elements_by_xpath("//input[@name='authorize' and @value='Permitir acceso']")
        python_mail = driver.find_element_by_name('session_key')
        python_mail.send_keys('juan.ohngemach@hotmail.com')
        python_password = driver.find_element_by_name('session_password')
        python_password.send_keys('Colt123456')
        python_button = driver.find_element_by_name('authorize')
        python_button.click()

        url = driver.current_url
        #Returned URL
        #print('\nFull Return URL:\n'+url)

        authentication.authorization_code = url.split('code=')[1].split('&')[0]

        print('\nAccess code:\n'+authentication.authorization_code+'\n')

        result = authentication.get_access_token()
        self.app_access_token = result.access_token

        #write access token to excel file
        rb = open_workbook("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/secrets.xls")
        wb = copy(rb)

        s = wb.get_sheet(0)
        s.write(self.app, 2, self.app_access_token)
        wb.save('/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/secrets.xls')
        
        #print("\nAccess Token:", result.access_token+'\n')
        #print("Expires in (seconds):", result.expires_in,'\n')

        driver.quit()

    def return_access_token(self):
        return self.app_access_token

# token_juan = ACCESS_TOKEN(3)
# print(token_juan.read_csv(3))


# token_juan = ACCESS_TOKEN(1)
# token_juan.register()
# print('SUCCESS '+token_juan.return_access_token())

# for i in range(1,5):
#     token_juan = ACCESS_TOKEN(i)
#     token_juan.register()

