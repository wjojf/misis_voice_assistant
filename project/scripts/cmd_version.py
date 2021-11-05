from spider import WebSpider
from recognizer import Recognizer
from speech_recognizer import SpeechRecognizer
from admin import AdminPanel
from time import sleep
from colorama import init, Fore, Back, Style


init(autoreset=True)
class VoiceAssistant:

	def __init__(self):

		self.recognizer = Recognizer()
		self.spider = WebSpider()
		self.speech_recognizer = SpeechRecognizer()
		self.admin_panel = AdminPanel()

		self.logged_in_file = '../assets/user_status/logged_in.txt'
	
	def greeting(self):
		print(Fore.YELLOW + '|---------------------------------|')
		print(Fore.YELLOW + '| Привет! Леонид начинает работу! |')
		print(Fore.YELLOW + '|---------------------------------|')


	def handle_user_command(self, user_command):

		'''
		Execute function if command understood,
		otherwise say command is not understood
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
        curr_password for saving data itself; logged_in for bool
        (True = logged, False = not)
        :param login: str -> login
        :param password: str -> user_password
        :return:
        '''

		# if password saved
		try:
			login, password = self.spider.get_user_data()
		
		# otherwise input password 
		except:
			login = input(Fore.MAGENTA + '[AUTH] m1111111@edu.misis.ru -> ')
			password = input(Fore.MAGENTA + '[AUTH] Пароль -> ')

		self.login = login

		with open('../assets/user_status/curr_password.txt', 'w', encoding='utf-8') as users_file:
			users_file.write(f'{login}|{password}')

		with open('../assets/user_status/logged_in.txt', 'w', encoding='utf-8') as status_file:
			status_file.write('True')

		print('[INFO] -> Получил данные пользователя')

	def run_cmd(self):
		'''
		Mainloop
		While command != quit: take new command, classify it and execute if classified
		:return: None
		'''

		self.authorize()

		print('[INFO] -> Начинаю работу...')

		#MAIN LOOP
		while True:

			user_input = input(Fore.GREEN + '[ВВОД] -> Что хотите сделать(/C:ввести команду, /Q: выйти)').lower()

			if user_input == '/c' or user_input == '/command':

				input_type = input(Fore.LIGHTYELLOW_EX + 'Голосом/Kлавиатурой: [/v, /k, /a(мод админа)]').lower()
				
				if input_type == '/v':

					try:
						user_command = self.speech_recognizer.take_command()

					except:
						user_command = None
				
					if self.speech_recognizer.is_valid(user_command):
					
						self.handle_user_command(user_command)
					
						sleep(2)
				
				elif input_type == '/k':
					command = input(Fore.GREEN + '[ВВОД] -> Введите команду: ')
					self.handle_user_command(command)


				# ADMIN MODE
				elif input_type == '/a':

					if self.admin_panel.user_is_admin(self.login):

						self.admin_panel.list()

						admin_command = input( Fore.RED + '[ADMIN] Введите команду -> ')

						if admin_command in self.admin_panel.commands_list:

							eval(f'self.admin_panel.{admin_command[1:]}()')





			elif user_input == '/q' or user_input == '/quit':
				self.exit()
				break



	def exit(self):
		print(Fore.YELLOW + '[INFO] -> Завершаю работу...')
		self.spider.exit()






if __name__ == '__main__':
	v = VoiceAssistant()
	v.greeting()
	v.run_cmd()