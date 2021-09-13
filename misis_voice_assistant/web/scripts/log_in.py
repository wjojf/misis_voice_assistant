import eel 
from spider import WebSpider


eel.init('../assets/UI')


class LoginPage:

	@eel.expose
	def save_login(login:str, password: str) -> bool:
		with open('../assets/passwords/curr_password.txt', 'w') as users_file:
			users_file.write(f'{login}|{password}')

	@eel.expose
	def start_spider() -> None:
		spider = WebSpider()
		spider.main()


	def _start(self):
		eel.start('index.html', size=(400, 400))




if __name__ == '__main__':
	app = LoginPage()
	app._start()
