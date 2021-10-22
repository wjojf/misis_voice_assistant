from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from colorama import init, Fore, Back, Style

class WebSpider:

	def __init__(self):
		self.driver = None
		self.info_page_driver = None

		# HTMLS
		self.ASSISTANT_INFO_HTML = '../assets/html/AssistantInfo.html'

		# AUTHORIZATION FILES
		self.logged_in_filepath = '../assets/user_status/logged_in.txt'
		self.password_filepath = '../assets/user_status/curr_password.txt'

		# URLS
		self.authorization_url = 'https://login.misis.ru/user/users/sign_in'
		self.LMS_URL = 'https://lms.misis.ru'
		self.LMS_COURSE_URL = self.LMS_URL + '/courses/'
		self.WEATHER_URL = 'https://www.gismeteo.ru/'
		self.INFO_URL = 'https://misis.ru/sveden/education/eduOp/'
		self.CURRICULUM_URL = 'https://login.misis.ru/ru/s68987/curriculum/index'
		self.SCHEDULE_URL =  'https://login.misis.ru/ru/s68987/schedule'
		self.RECORDBOOK_URL = 'https://login.misis.ru/ru/s68987/stud-book?type=mark'
		self.WIFI_INFO_URL = 'https://login.misis.ru/ru/s68987/wifis'
		self.SERVICES_URL = 'https://login.misis.ru/ru/s68987/rqsvc_requests'
		self.STUDENT_CARD_INFO_URL = 'https://login.misis.ru/ru/s68987/stud_registry'
		
		# USER STATUS
		self.logged_in = False
		self.save_password = False
		self.delete_password = True


	def _print(self, message):
		print(Fore.YELLOW + message)

	def show_error_html(self, error_message):
		'''
		Opens a page with local html error message
		:param error_message:
		:return:
		'''
		if self.driver:
			html_content = f'<html>{error_message}</html>'
			self.driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))

		else:
			self.driver = webdriver.Chrome(ChromeDriverManager().install())
			self.show_error_html(error_message)

	def show_assistant_info(self):
		'''

		:return: None
		'''

		if self.info_page_driver:

			try:
				html_content = open(self.ASSISTANT_INFO_HTML, encoding='utf-8').read()
				self.info_page_driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))

			except Exception as e:
				self.show_error_html(str(e))
			
			sleep(10)
			self.info_page_driver.quit()
		
		else:
			self.info_page_driver = webdriver.Chrome(ChromeDriverManager().install())
			self.show_assistant_info()

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

	def ask_save_password(self):
		'''
		Change status for saving password after exit
		:return: None
		'''


		user_answer = input('[INPUT] -> Save password?(y/n): ')

		if user_answer.lower() in ['yes', 'y']:
			self.save_password = True
			self.delete_password = False



			return

		elif user_answer.lower() in ['no', 'n']:
			self.save_password = False
			self.delete_password = True
			return

		else:
			self._print('[ERROR] -> Command not recognized')
			self.ask_save_password()

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
			with open(self.logged_in_filepath, 'w', encoding='utf-8') as file:
				file.write('True')



		
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		
		
		try:

			login, password = self.get_user_data()

		
			self.driver.get(self.authorization_url)
		
			try:
				login_element = self.driver.find_element_by_id('user_login')
				login_element.send_keys(login)
			
			except:
				self._print('[ERROR] -> Cannot find login element on page:(')
				return

			try:
				password_element = self.driver.find_element_by_id('user_password')
				password_element.send_keys(password)
			
			except:
				self._print('[ERROR] -> Не могу найти поле для ввода пароля:(')
				return 
			
			try:
				button_element = self.driver.find_element_by_name('commit')
				button_element.click()
			
			except:
				self._print('[ERROR] -> Не могу найти кнопку ввода:(')
				return 
		
			curr_url = self.driver.current_url

			#IF LOGGED IN
			if curr_url.split('/')[-2] == 'services':
				self._print('[SELENIUM INFO] -> Успешно выполнен вход!')
				self.logged_in = True
				write_log_in()

					
			else:
				html_content = open(self.WrongLoginPasswordError_html).read()
				self.driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))


		except ValueError:
			self._print('[ERROR] Не смог найти данные пользователя ->', self.get_user_data())
			self.show_error_html('Не смог найти данные пользователя:(')

	


	def show_schedule(self):
		'''
		Open schedule page on university website
		:return: None
		'''

		if not self.logged_in:
			self.log_in()
			
		if self.logged_in:
			#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/schedule
			try:
				self.driver.get(self.SCHEDULE_URL)
				sleep(5)
			except Exception as e:
				self.show_error_html(str(e))

		

	def show_curriculum(self):
		'''
		Open curriculum page on university website
		:return: None
		'''


		if not self.logged_in:
			self.log_in()

		
		#https://login.misis.ru/ru/s68987/services/index -> https://login.misis.ru/ru/s68987/curriculum/index
		if self.logged_in:
			try:
				self.driver.get(self.CURRICULUM_URL)
				sleep(5)
			except Exception as e:
				self.show_error_html(str(e))
		
		

	def show_info(self):
		'''
		Open info page on university website
		:return: None
		'''


		if not self.logged_in:
			self.log_in()
		

		if self.logged_in:

			try:
				self.driver.get(self.INFO_URL)
				sleep(5)
			except Exception as e:
				self.show_error_html(str(e))

	def authorize_lms(self):
		'''
		authorize on lms.misis.ru -> opens home courses page
		:return:
		'''
		try:
			email, password = self.get_user_data()
		
		except ValueError:
			self._print('[SELENIUM ERROR] -> user data: ', self.get_user_data())
			self.show_error_html('Cannot get user data:(')

			return

		try:
			login_element = self.driver.find_element_by_id("pseudonym_session_unique_id")
			password_element = self.driver.find_element_by_id("pseudonym_session_password")
			button_element = self.driver.find_element_by_css_selector("#login_form > div.ic-Login__actions > div.ic-Form-control.ic-Form-control--login > button")
			
			login_element.send_keys(email)
			password_element.send_keys(password)
			button_element.click()

		except:
			self._print('[SELENIUM ERROR] -> Cannot find elements on page')
			self.show_error_html('[SELENIUM ERROR] -> Cannot find elements on page')

	def open_lms(self):
		'''
		Open lms.misis.ru and authorizes
		:return: None
		'''
		if not self.logged_in:
			self.log_in()


		if self.logged_in:
			self.driver.get(self.LMS_URL)

			try:
				self.authorize_lms()

			except Exception as e:
				self.show_error_html(str(e))


	def show_courses_lms(self):
		'''
		Prints list of courses on canvas
		:return: None
		'''
		if self.driver:

			if self.LMS_URL in self.driver.current_url:
				courses = self.driver.find_elements_by_class_name('ic-DashboardCard')
				for n, course in enumerate(courses):
					print(f'{n + 1})', course.get_attribute("aria-label"))
					print()
			else:
				self._print('[ERROR] -> Вы не на платформе LMS Canvas. Скажите "октрой канвас" или что-то похоже...')
				self.show_error_html('[ERROR] -> Вы не на платформе LMS Canvas. Скажите "октрой канвас" или что-то похоже...')


	
	def open_course_lms(self):
		'''
		Prints list of courses and clicks on/opens chosen
		:return: None
		'''
		if self.driver:
			self._print('[ANSWER] -> Вот все курсы: ')

			self.show_courses_lms()

			course_index = int(input('Введите номер курса: '))

			courses = self.driver.find_elements_by_class_name('ic-DashboardCard')

			try:
				self._print(f'[ANSWER] -> Отрываю курс {course_index}')
				courses[course_index - 1].click()

			except IndexError:
				self._print(f'[ERROR] -> нет курса с номером {course_index}')
				self.show_error_html(f'[ERROR] -> нет курса с номером {course_index}')

	# TODO:
	def open_homework_lms(self):
		
		if self.logged_in:
			if self.LMS_COURSE_URL in self.driver.current_url:
				section_list = self.driver.find_element_by_id('section-tabs').find_elements_by_tag_name('li')
				
				for action_element in section_list:
					if action_element.text == 'Задания':
						action_element.click()
						return 
			
			else:
				self._print('[ANSWER] -> Вы не на платформе Canvas. Cкажите мне её открыть')



	def open_recordbook(self):
		'''
		Open online recordbook
		:return:
		'''
		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.RECORDBOOK_URL)
			except:
				self._print('[SELENIUM ERROR] -> Cannot open recordbook')
				self.show_error_html('[SELENIUM ERROR] -> Cannot open recordbook')

	def show_weather(self):
		'''
		Opens a weather forecast site
		:return:
		'''
		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.WEATHER_URL)
			except:
				self._print('[SELENIUM ERROR] -> CANNOT OPEN WEATHER SITE')
				self.show_error_html('[SELENIUM ERROR] -> CANNOT OPEN WEATHER SITE')

	def show_wifi_info(self):
		'''
		Opens wi-fi info page on misis website
		:return:
		'''
		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.WIFI_INFO_URL)
			except Exception as e:
				self._print(f'[ERROR] -> {e}')
				self.show_error_html(str(e))

	def show_services(self):
		'''
		Opens services page on misis website
		:return:
		'''
		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.SERVICES_URL)
			except Exception as e:
				self._print(f'[ERROR] -> {e}')
				self.show_error_html(str(e))

	def show_student_id_info(self):
		'''
		Opens studentID card page
		:return:
		'''
		if not self.logged_in:
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.STUDENT_CARD_INFO_URL)
			except Exception as e:
				self._print(f'[ERROR] -> {e}')
				self.show_error_html(str(e))

	def exit(self):

		'''
		Close WebDriver, write user status
		:return:
		'''
		self.ask_save_password()

		if self.logged_in:

			self.logged_in = False


			if self.delete_password:

				with open(self.logged_in_filepath, 'w') as logged_in_file:
					logged_in_file.write('False')

				with open(self.password_filepath, 'w') as password_file:
					password_file.write('')


		try:
			self.driver.close()
		except:
			pass





