import sys
from selenium import webdriver
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains




class NEW_ACCOUNTS:
	def __init__(self,app_name,description,website, mail, telephone, row):
		self.app_name = app_name
		self.description = description
		self.website = website
		self.mail = mail
		self.telephone = telephone
		self.row = row

	def create(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--test-type")
		driver = webdriver.Chrome('/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/renew_token/chromedriver')
		driver.get('https://www.linkedin.com/developer/apps/')
		delay = 3 # seconds


		try:
		    python_sign_in = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'sign-in-link')))
		    python_sign_in.click()
		    print ("Page is ready!")
		except TimeoutException:
		    print( "Loading took too much time!")


		#python_button = driver.find_elements_by_xpath("//input[@name='authorize' and @value='Permitir acceso']")
		# python_sign_in = driver.find_element_by_class_name('sign-in-link')
		# python_sign_in.click()

		try:
		    python_mail = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'session_key')))
		    python_mail.send_keys('juan.ohngemach@hotmail.com')
		    python_password = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'session_password')))
		    python_password.send_keys('Colt123456')
		    python_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'signin')))    
		    python_button.click()
		    print ("Page is ready!")
		except TimeoutException:
		    print( "Loading took too much time!")

		try:
		    python_create_new = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'button-create-application')))
		    python_create_new.click()
		    print ("Page is ready!")
		except TimeoutException:
		    print( "Loading took too much time!")

		try:
		    python_create_name = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'name')))
		    python_create_name.send_keys(self.app_name)
		    python_create_desc = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'description')))
		    python_create_desc.send_keys(self.description)
		    
		    driver.find_element_by_name("appLogo").send_keys("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/developer_accounts/logo.png")

		    #driver.switch_to.active_element.send_keys("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/developer_accounts/logo.png")

		    # python_create_upload = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'submit-button')))
		    # python_create_upload.send_keys('l')
		    # python_create_upload.send_keys(Keys.RETURN)



		    python_create_name.find_element_by_xpath("//select[@name='use']/option[text()='Other']").click()

		    python_create_website = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'websiteUrl')))
		    python_create_website.send_keys(self.website)
		   
		    python_create_mail = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'businessEmail')))
		    python_create_mail.send_keys(self.mail)

		    # python_create_terms = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'terms')))
		    # python_create_terms.send_keys(self.mail)

		    driver.find_element_by_css_selector("input[type='checkbox']").click()


		 #    driver.find_element_by_xpath(
			#     ".//*[contains(text(), 'Ich habe die')]"
			# ).click()


		    python_create_phone = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'businessPhone')))
		    python_create_phone.send_keys(self.telephone)

		    python_create_submit = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, ".//*[contains(text(), 'Senden')]")))
		    python_create_submit.click()



		    print ("Page is ready! Submitting application...")

		except TimeoutException:
		    print( "Loading took too much time!")
		
		try:

			# python_configure_r_email = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'r_emailaddress[]')))
			# python_configure_r_email.click()

			# python_configure_r_comp_admin = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'rw_company_admin[]')))
			# python_configure_r_comp_admin.click()

			# python_configure_r_share = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'w_share[]')))
			# python_configure_r_share.click()

			python_configure_URL = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'oauth2-redirectUrl-input')))
			python_configure_URL.send_keys('http://localhost:8080/code/')

			python_configure_add_URL = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'add-row')))
			python_configure_add_URL.click()

			print ("Application configured!")

			CLIENT_ID = driver.find_element_by_xpath("//span[@aria-describedby='apiKey-tooltip']")
			CLIENT_SECRET = driver.find_element_by_xpath("//span[@aria-describedby='secretKey-tooltip']")

			print("\nCLIENT_ID: "+CLIENT_ID.text)
			print("\nCLIENT_SECRET: "+CLIENT_SECRET.text)

			rb = open_workbook("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/developer_accounts/account_names.xls")
			wb = copy(rb)
			s = wb.get_sheet(0)
			s.write(self.row, 5, CLIENT_ID.text)
			s.write(self.row, 6, CLIENT_SECRET.text)
			wb.save("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/developer_accounts/account_names.xls")

			#driver.close()
		except TimeoutException:
		    print( "Loading took too much time!")
		



		





app_name = ''
description = ''
website = ''
mail = ''
telephone  = ''
row = ''
book = xlrd.open_workbook("/Users/juanruizdebustillo/GitHub/Telepy-Linkedin_TFG/developer_accounts/account_names.xls")
sh = book.sheet_by_index(0)
for rx in range(1,sh.nrows):    

	app_name = sh.row(rx)[0].value
	description = sh.row(rx)[1].value
	website = sh.row(rx)[2].value
	mail = sh.row(rx)[3].value
	telephone = str(sh.row(rx)[4].value).strip('.').rstrip('0').strip('.')
	row = rx

	print('App: '+sh.row(rx)[0].value)
	print('Desc: '+sh.row(rx)[1].value)
	print('Website: '+sh.row(rx)[2].value)
	print('Mail: '+sh.row(rx)[3].value)
	print('Tel: '+telephone)
	print('Row: '+str(row))

	juans_new_account = NEW_ACCOUNTS(app_name, description, website, mail, telephone, row)

	juans_new_account.create()






