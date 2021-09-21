from log_in import LoginPage
from spider import WebSpider
from recognizer import Recognizer
from speech_recognizer import SpeechRecognizer
from time import sleep
import sys


class VoiceAssistant:

	def __init__(self):
		self.logged_in_file = '../assets/user_status/logged_in.txt'
		self.recognizer = Recognizer()
		self.login_page = LoginPage()
		self.spider = WebSpider()
		self.sr = SpeechRecognizer()

	
	def handle_user_command(self, user_command):

		'''
		Execute function if command understood, otherwise say command is not understood
		:param user_command: str
		:return: None
		'''

		func = self.recognizer.get_func(user_command)
		self.sr.say(func['answer'])
		if func['func'] is not None:
			
			eval(func['func'])

			sleep(2)


	def run(self):
		'''
		Mainloop
		While command != quit: take new command, classify it and execute if classified
		:return: None
		'''

		print('[INFO] -> STARTING...')


		while True:

			user_input = input('[INPUT] -> Input action(/C:command, /Q: quit)').lower()

			if user_input == '/c' or user_input == '/command':
				input_type = input('Voice/Keyboard: [/v, /k]').lower()
				
				if input_type == '/v':
					try:
						user_command = self.sr.take_command()
					except:
						user_command = None
				
					if self.sr.is_valid(user_command):
					
						self.handle_user_command(user_command)
					
						sleep(2)
				
				elif input_type == '/k':
					command = input('[KEYBOARD_INPUT] -> Введите команду: ')
					self.handle_user_command(command)

			elif user_input == '/q' or user_input == '/quit':
				break



	def exit(self):
		self.spider.exit()
		sys.exit(1)


if __name__ == '__main__':
	v = VoiceAssistant()
	v.run()