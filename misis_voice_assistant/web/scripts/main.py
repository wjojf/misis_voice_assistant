from log_in import LoginPage
from spider import WebSpider
from recognizer import Recognizer
from time import sleep
import sys

class VoiceAssistantGUI:


	def __init__(self):
		self.logged_in_file = '../assets/passwords/logged_in.txt'
		self.recognizer = Recognizer()
		self.login_page = LoginPage()
		self.spider = WebSpider()


	def is_logged_in(self):
		with open(self.logged_in_file, 'r') as file:
			return eval(file.readline())

	def is_valid_command(self, command):
		return command != 'Error!'

	#TODO:
	def run_gui(self):
		pass


	def start(self):
		self.login_page._start()

		#It stops working here without throwing any errors. 
		#TODO: WHY??

		print('Got user data!')
		sleep(10)
		
		if self.is_logged_in():
			
			test_command = 'Покажи-ка расписание на завтра'

			command = self.recognizer.get_command(test_command)

			if self.is_valid_command(command):
				eval(command)
				sleep(2)

			test_command = 'выйди'
			command = self.recognizer.get_command(test_command)
			
			if self.is_valid_command(command):
				eval(command)
				sleep(2)

		else: 
			print('Не вошёл')

	

	def exit(self):
		self.spider.exit()




if __name__ == '__main__':
	v = VoiceAssistantGUI()
	v.start()