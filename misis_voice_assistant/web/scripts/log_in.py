import eel 
from spider import WebSpider
from time import sleep
import sys

eel.init('../assets/login_page')


class LoginPage:

	

	@eel.expose
	def save_login(self, login: str, password: str) -> bool:
		'''
		Store user data into files
		curr_password for saving data itself; logged_in for bool (True = logged, False = not)
		:param login: str -> user_login
		:param password: str -> user_password
		:return:
		'''


		with open('../assets/user_status/curr_password.txt', 'w') as users_file:
			users_file.write(f'{login}|{password}')
		
		with open('../assets/user_status/logged_in.txt', 'w') as status_file:
			status_file.write('True')

		print('[INFO] -> Saved user data')
	
	
	def _start(self):
		eel.start('index.html', size=(500, 500))


