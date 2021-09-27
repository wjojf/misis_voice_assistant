from spider import WebSpider
from recognizer import Recognizer
from speech_recognizer import SpeechRecognizer
from admin import AdminPanel
from time import sleep
from colorama import init, Fore, Back, Style
import sys

init(autoreset=True)
class VoiceAssistant:

	def __init__(self):
		self.logged_in_file = '../assets/user_status/logged_in.txt'
		self.recognizer = Recognizer()
		self.spider = WebSpider()
		self.speech_recognizer = SpeechRecognizer()
		self.admin_panel = AdminPanel()

	
	def handle_user_command(self, user_command):

		'''
		Execute function if command understood, otherwise say command is not understood
		:param user_command: str
		:return: None
		'''

		func = self.recognizer.get_func(user_command)
		self.speech_recognizer.say(func['answer'])
		if func['func'] is not None:
			
			eval(func['func'])

			sleep(2)


	def authorize(self):
		'''
        Store user data into files
        curr_password for saving data itself; logged_in for bool (True = logged, False = not)
        :param login: str -> user_login
        :param password: str -> user_password
        :return:
        '''
		login = input('[AUTH] m1111111@edu.misis.ru -> ')
		password = input('[AUTH] password -> ')

		self.user_login = login

		with open('../assets/user_status/curr_password.txt', 'w') as users_file:
			users_file.write(f'{login}|{password}')

		with open('../assets/user_status/logged_in.txt', 'w') as status_file:
			status_file.write('True')

		print('[INFO] -> Saved user data')

	def run(self):
		'''
		Mainloop
		While command != quit: take new command, classify it and execute if classified
		:return: None
		'''

		self.authorize()

		print('[INFO] -> STARTING...')

		#MAIN LOOP
		while True:

			user_input = input('[INPUT] -> Input action(/C:command, /Q: quit)').lower()

			if user_input == '/c' or user_input == '/command':

				input_type = input('Voice/Keyboard: [/v, /k, /a(admins only)]').lower()
				
				if input_type == '/v':

					try:
						user_command = self.speech_recognizer.take_command()

					except:
						user_command = None
				
					if self.speech_recognizer.is_valid(user_command):
					
						self.handle_user_command(user_command)
					
						sleep(2)
				
				elif input_type == '/k':
					command = input('[KEYBOARD_INPUT] -> Введите команду: ')
					self.handle_user_command(command)


				# ADMIN MODE
				elif input_type == '/a':

					if self.admin_panel.user_is_admin(self.user_login):

						self.admin_panel.list()

						admin_command = input('[ADMIN] Enter command -> ')

						if admin_command in self.admin_panel.commands_list:

							eval(f'self.admin_panel.{admin_command[1:]}()')





			elif user_input == '/q' or user_input == '/quit':
				self.exit()
				break



	def exit(self):
		print('[INFO] -> Завершаю работу...')
		self.spider.exit()






if __name__ == '__main__':
	v = VoiceAssistant()
	v.run()