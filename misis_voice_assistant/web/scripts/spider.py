from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json 



class WebSpider:


	def __init__(self):

		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.driver.implicitly_wait(30)
		
		self.autorization_url = 'https://login.misis.ru/user/users/sign_in'
		self.logged_in_filepath = '../assets/passwords/logged_in.txt'
		self.password_filepath = '../assets/passwords/curr_password.txt'
		
		self.file_is_empty_error_html = None
		self.login_is_wrong_error_html = None
		self.WrongLoginPasswordError_html = None

	
	def get_user_data(self):

		try:
			with open(self.password_filepath) as file:
				return file.readline().split('|')
		except:
			return 'Error!'


	def write_log_in(self):
		with open(self.logged_in_filepath, 'w') as file:
			file.write('True')


	def log_in(self):

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
				self.write_log_in()
			
			else:
				self.driver.get(WrongLoginPasswordError_html)


		except ValueError:
			self.driver.get(file_is_empty_error_html)
			#print(self.password_filepath)

	def show_schedule(self):

		self.log_in()
		
		if self.logged_in:
			curr_url = self.driver.current_url.split('/')

			#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/schedule
			schedule_url =  '/'.join(curr_url[:-2] + ['schedule'])
			try:
				self.driver.get(schedule_url)
			except Exception as e:
				print(e)

	def show_curriculum(self):

		self.log_in()

		if self.logged_in:
			#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/curriculum/index

			curr_url = self.driver.current_url.split('/')
			curriculum_url = '/'.join(curr_url[:-2] + ['curriculum', 'index'])

			try:
				self.driver.get(curriculum_url)
			except Exception as e:
				print(e)




