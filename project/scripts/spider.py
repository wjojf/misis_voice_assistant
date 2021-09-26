from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json 
import sys



class WebSpider:


	def __init__(self):

		self.autorization_url = 'https://login.misis.ru/user/users/sign_in'
		self.logged_in_filepath = '../assets/user_status/logged_in.txt'
		self.password_filepath = '../assets/user_status/curr_password.txt'
		
		self.file_is_empty_error_html = '../assets/errors/file_is_empty.html'
		self.WrongLoginPasswordError_html = '../assets/errors/wrong_login.html'

		#URLS
		self.LMS_URL = 'https://lms.misis.ru/'
		self.WIFI_INFO_URL = 'https://login.misis.ru/ru/s68987/wifis'
		self.SERVICES_URL = 'https://login.misis.ru/ru/s68987/rqsvc_requests'

		#boolean
		self.logged_in = False

	def get_user_data(self):
		'''
		Get user data from .txt file
		:return: [login, password]
		'''

		try:
			with open(self.password_filepath) as file:
				return file.readline().split('|')
		except:
			return 'Error!'



	def log_in(self):
		'''
		1)Write logged in status for user

		2)Open WebDriver

		3)Try to log in on site

		4)If logged in change self.logged_in -> True
				else handle all possible errors(wrong login, site not working, etc...)

		:return:None
		'''


		def write_log_in():
			with open(self.logged_in_filepath, 'w') as file:
				file.write('True')

		
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		
		
		try:

			login, password = self.get_user_data()

		
			self.driver.get(self.autorization_url)
		
			try:
				login_element = self.driver.find_element_by_id('user_login')
				login_element.send_keys(login)
			
			except:
				print('Cannot find login element on page:(')
				return

			try:
				password_element = self.driver.find_element_by_id('user_password')
				password_element.send_keys(password)
			
			except:
				print('Cannot find password element on page:(')
				return 
			
			try:
				button_element = self.driver.find_element_by_name('commit')
				button_element.click()
			
			except:
				print('Cannot find button on page:(')
				return 
		
			curr_url = self.driver.current_url

			if curr_url.split('/')[-2] == 'services':
				print('[INFO] -> Succesfully logged in!')
				self.logged_in = True
				write_log_in()
					
			else:
				html_content = open(self.WrongLoginPasswordError_html).read()
				self.driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))


		except ValueError:
			print(self.get_user_data())
			html_content = open(self.file_is_empty_error_html).read()
			self.driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))

	


	def show_schedule(self):
		'''
		Open schedule page on university website
		:return: None
		'''

		if not self.logged_in:
			self.log_in()
			
		if self.logged_in:
			
			#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/schedule
			schedule_url =  'https://login.misis.ru/ru/s68987/schedule'
			try:
				self.driver.get(schedule_url)
				sleep(5)
			except Exception as e:
				print(e)

		

	def show_curriculum(self):
		'''
		Open curriculum page on university website
		:return: None
		'''


		if not self.logged_in:
			self.log_in()

		
		#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/curriculum/index
		if self.logged_in:
			
			curriculum_url = 'https://login.misis.ru/ru/s68987/curriculum/index'
			
			try:
				self.driver.get(curriculum_url)
				sleep(5)
			except Exception as e:
				print(e)
		
		

	def show_info(self):
		'''
		Open info page on university website
		:return: None
		'''


		if not self.logged_in:
			self.log_in()
		

		if self.logged_in:
			info_url = 'https://misis.ru/sveden/education/eduOp/'
			try:
				self.driver.get(info_url)
				sleep(5)
			except Exception as e:
				print(e)

	def authorize_lms(self):
		try:
			email, password = self.get_user_data()
		
		except ValueError:
			print('[ERROR] -> user data: ', self.get_user_data())
			html_content = open(self.file_is_empty_error_html).read()
			self.driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))

			return

		try:
			login_element = self.driver.find_element_by_id("pseudonym_session_unique_id")
			password_element = self.driver.find_element_by_id("pseudonym_session_password")
			button_element = self.driver.find_element_by_css_selector('login_form > div.ic-Login__actions > div.ic-Form-control.ic-Form-control--login > button')
			
			login_element.send_keys(email)
			password_element.send_keys(password)
			button_element.click()

		except:
			print('[ERROR] Cannot find elements on page')


	def open_lms(self):

		if not(self.logged_in):
			self.log_in()

		

		if self.logged_in:
			self.driver.get(self.LMS_URL)

			try:
				self.authorize_lms()

			except Exception as e:
				print(e)


	def show_wifi_info(self):

		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.WIFI_INFO_URL)

			except Exception as e:
				print(e)


	def show_services(self):

		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.SERVICES_URL)
			except Exception as  e:
				print(e)




	def exit(self):

		'''
		Close WebDriver, write user status
		:return:
		'''

		if self.logged_in:
			self.logged_in = False

			with open(self.logged_in_filepath, 'w') as logged_in_file:
				logged_in_file.write('False')

			with open(self.password_filepath, 'w') as password_file:
				password_file.write('')

			sleep(1)

			self.driver.close()




