from log_in import LoginPage
from spider import WebSpider
from recognizer import Recognizer
import sys

class VoiceAssistantGUI:


	def __init__(self):
		self.logged_in_file = '../assets/passwords/logged_in.txt'
		self.recognizer = Recognizer()
		self.login_page = LoginPage()


	def is_logged_in(self):
		with open(self.logged_in_file, 'r') as file:
			return eval(file.readline())

	#TODO:
	def run_gui(self):
		pass


	def start(self):
		self.login_page._start()

		if self.is_logged_in():
			self.run_gui()

	def exit(self):
		with open(self.logged_in_file, 'w') as file:
			file.write('False')
		
		sys.exit()


