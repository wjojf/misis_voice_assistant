import tkinter
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import simpledialog
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
		self.GOOGLE_SERVICES_URL = 'https://login.misis.ru/ru/s68987/services/google'
		self.GMAIL_URL = 'https://mail.google.com/a/edu.misis.ru/'
		
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
			
			sleep(8)
			self.info_page_driver.quit()
			self.info_page_driver = None
		
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

		#print(Fore.RED + f'[DEBUG] -> {user_answer}')

		if user_answer.lower() in ['yes', 'y']:
			self.save_password = True
			self.delete_password = False
			#print('save')


			return

		elif user_answer.lower() in ['no', 'n']:
			#print('delete')
			self.save_password = False
			self.delete_password = True

			return

		else:
			self._print('[ОШИБКА] -> Команда не распознана')
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
				self._print('[ОШИБКА] -> Не смог найти поле для логина:(')
				return

			try:
				password_element = self.driver.find_element_by_id('user_password')
				password_element.send_keys(password)
			
			except:
				self._print('[ОШИБКА] -> Не могу найти поле для ввода пароля:(')
				return 
			
			try:
				button_element = self.driver.find_element_by_name('commit')
				button_element.click()
			
			except:
				self._print('[ОШИБКА] -> Не могу найти кнопку ввода:(')
				return 
		
			curr_url = self.driver.current_url

			#IF LOGGED IN
			if curr_url.split('/')[-2] == 'services':
				self._print('[SELENIUM] -> Успешно выполнен вход!')
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
			self._print('[ОШИБКА SELENIUM] -> user data: ', self.get_user_data())
			self.show_error_html('Cannot get user data:(')

			return

		try:
			login_element = self.driver.find_element_by_id("pseudonym_session_unique_id")
			password_element = self.driver.find_element_by_id("pseudonym_session_password")
			button_element = self.driver.find_element_by_css_selector("#login_form > div.ic-Login__actions > div.ic-Form-control.ic-Form-control--login > button")
			
			login_element.send_keys(email)
			password_element.send_keys(password)
			button_element.click()

		except: # ALREADY AUTHORIZED
			pass

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
			self._print('[Леонид] -> Вот все курсы: ')

			self.show_courses_lms()

			course_index = int(input('Введите номер курса: '))

			courses = self.driver.find_elements_by_class_name('ic-DashboardCard')

			try:
				self._print(f'[Леонид] -> Отрываю курс {course_index}')
				courses[course_index - 1].click()

			except IndexError:
				self._print(f'[ОШИБКА] -> нет курса с номером {course_index}')
				self.show_error_html(f'[ОШИБКА] -> нет курса с номером {course_index}')


	def open_homework_lms(self):
		
		if self.logged_in:
			if self.LMS_COURSE_URL in self.driver.current_url:
				section_list = self.driver.find_element_by_id('section-tabs').find_elements_by_tag_name('li')
				
				for action_element in section_list:
					if action_element.text == 'Задания':
						action_element.click()
						return 
			
			else:
				self._print('[Леонид] -> Вы не на платформе Canvas. Cкажите мне её открыть')



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
				self._print('[ОШИБКА SELENIUM] -> Не могу открыть зачёту')
				self.show_error_html('[ОШИБКА SELENIUM] -> Не могу открыть зачётку')

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
				self._print('[ОШИБКА SELENIUM] -> Не смог открыть прогноз погоды')
				self.show_error_html('[ОШИБКА SELENIUM] -> Не смог открыть прогноз погоды')

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
				self._print(f'[ОШИБКА] -> {e}')
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
				self._print(f'[ОШИБКА] -> {e}')
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
				self._print(f'[ОШИБКА] -> {e}')
				self.show_error_html(str(e))

	#TODO:
	def open_email(self):

		if not(self.logged_in):
			self.log_in()

		if self.logged_in:
			try:
				self.driver.get(self.GOOGLE_SERVICES_URL)
				'''
				<div class="col-sm-2" style="padding-top: 20px; padding-bottom: 20px;"><a href="https://mail.google.com/a/edu.misis.ru/"> <span>Gmail</span></a></div>
				'''
				gmail_element = self.driver.find_elements_by_class_name('col-sm-2')[0]
				try:
					gmail_element.click()
				except Exception as e:
					self._print(f'[ОШИБКА] -> {e}')
					self.show_error_html(str(e))
			except Exception as e:
				self._print(f'[ОШИБКА] -> {e}')
				self.show_error_html(str(e))

	#TODO:
	def log_in_gmail(self):

		user_data = self.get_user_data()

		gmail_login = user_data[0].split('@')[0]

		same_password = input(Fore.YELLOW + '[ВВОД] -> пароли для почты и ЛК совпадают?(y/n): ').lower()

		if same_password in ['y', 'yes']:
			gmail_password = user_data[1]

		elif same_password in ['n', 'no']:
			gamil_password = input(Fore.MAGENTA + '[ВВОД] -> Пароль для gmail: ')

		if gmail_login and gamil_password:
			try:
				password_element = self.driver.find_element_by_id('password')
				password_element.send_keys(gmail_password)

				try:
					submit_element = self.driver.find_element_by_xpath('//button')
					submit_element.click()

				except Exception as e:

					self._print(f'[ОШИБКА] -> {e}')
					self.show_error_html(str(e))

			except Exception as e:
				self._print(f'[ОШИБКА] -> {e}')
				self.show_error_html(str(e))







	def exit(self):

		'''
		Close WebDriver, write user status
		:return:
		'''
		self.ask_save_password()

		if self.logged_in:

			self.logged_in = False


			if not(self.save_password):

				with open(self.logged_in_filepath, 'w') as logged_in_file:
					logged_in_file.write('False')

				with open(self.password_filepath, 'w') as password_file:
					password_file.write('')

				with open('../assets/passwords/password_saved.txt', 'w') as f:
					f.write('False')
			else:
				with open('../assets/passwords/password_saved.txt', 'w') as f:
					f.write('True')


		try:
			self.driver.close()
		except:
			pass


	# GUI FUNCS
	def ask_save_password_gui(self):
		msg = tkinter.Tk()
		msg.withdraw()

		save_password = simpledialog.askstring('Сохранить пароль?', "Сохранить пароль(y/n)?", parent=msg)

		if save_password.lower() in ['y', 'yes']:
			return True

		elif save_password.lower() in ['n', 'no']:

			return False

		self.ask_save_password_gui()


	def exit_gui(self):


		save_password = self.ask_save_password_gui()
		print(save_password)

		if self.logged_in:

			self.logged_in = False


		if save_password:
			with open('../assets/passwords/password_saved.txt', 'w') as f:
				f.write('True')

		else:
			#print('Rewriting data')
			with open(self.logged_in_filepath, 'w') as logged_in_file:
				logged_in_file.write('False')

			with open(self.password_filepath, 'w') as password_file:
				password_file.write('')

			with open('../assets/passwords/password_saved.txt', 'w') as f:
				f.write('False')

		try:
			self.driver.close()
		except:
			pass


