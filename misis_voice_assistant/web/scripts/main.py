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

		func = self.recognizer.get_func(user_command)

		if func['func'] is not None:
			self.sr.say(func['answer'])
			eval(func['func'])

			sleep(2)

	def run(self):
		print('[INFO] -> STARTING...')


		while True:

			user_command = self.sr.take_command()

			if self.sr.is_valid(command)
			self.handle_user_command(user_command)




	def exit(self):
		self.spider.exit()
		sys.exit(1)


if __name__ == '__main__':
	v = VoiceAssistant()
	v.run()