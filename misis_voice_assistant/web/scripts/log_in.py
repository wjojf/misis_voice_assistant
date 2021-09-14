import eel 
from spider import WebSpider


eel.init('../assets/UI')


class LoginPage:

	@eel.expose
	def save_login(login:str, password: str) -> bool:
		with open('../assets/passwords/curr_password.txt', 'w') as users_file:
			users_file.write(f'{login}|{password}')

	
	def _start(self):
		eel.start('index.html', size=(400, 400))



#LoginPage()._start()