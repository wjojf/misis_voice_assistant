from colorama import init, Fore, Back, Style
import json

init(autoreset=True)
class AdminPanel:

	def __init__(self):
		self.ADMINS_FILEPATH = '../assets/user_status/admins.json'
		self.INTENTS_FILEPATH = '../assets/intents_json'
		self.BANNED_FILEPATH = '../assets/user_status/banned.json'
		self.commands_list = ['/list', '/add_keyword', '/add_answer', '/add_func', '/ban']

	def user_is_admin(self, user):
		admins_list = json.loads(open(self.ADMINS_FILEPATH, 'r', encoding='utf-8').read())['users']

		return user.lower() in admins_list

	def ban(self):
		user_to_ban = input('[АДМИН] -> юзер для бана: ')

		admins_list = json.loads(open(self.ADMINS_FILEPATH, 'r', encoding='utf-8').read())['users']

		if user_to_ban.lower() not in admins_list:
			with open(self.BANNED_FILEPATH)	as banned_file:
				banned_users = json.loads(banned_file.read())

			banned_users['users'].append(user_to_ban.lower())

			with open(self.BANNED_FILEPATH, 'w') as banned_file:
				json.dump(banned_users, banned_file)
				print(f'[INFO] Успешно забанен пользователь {user_to_ban}')


	def list(self):
		print(Fore.RED + '[РЕЖИМ АДМИНА]')
		print('Cписок команд админа: ')

		for command in self.commands_list:
			print(Fore.GREEN + f'[КОМАНДА] -> {command}')


	def add_keyword(self):
		keywords_filepath = self.INTENTS_FILEPATH + '/intents_and_keywords.json'

		intent = input(Fore.RED + '[ADMIN INPUT] Enter intent ->')
		keyword = input(Fore.RED + '[ADMIN INPUT] Enter keyword ->')

		with open(keywords_filepath, 'r', encoding='utf-8') as json_file:
			intents_and_keywords = json.loads(json_file.read())

		if intent in intents_and_keywords:
			intents_and_keywords[intent].append(keyword)
			intents_and_keywords[intent] = list(set(intents_and_keywords[intent]))

		with open(keywords_filepath, 'w', encoding='utf-8') as json_file:
			json.dump(intents_and_keywords, json_file)
			print(f'[INFO] -> Successfully added {keyword} to {intent}')


	def add_answer(self):
		answers_filepath = self.INTENTS_FILEPATH + '/intents_and_answers.json'

		intent = input(Fore.RED + '[ADMIN INPUT] Enter intent ->')
		answer = input(Fore.RED + '[ADMIN INPUT] Enter answer ->')

		with open(answers_filepath, 'r', encoding='utf-8') as json_file:
			intents_and_answers = json.loads(json_file.read())


		if intent in intents_and_answers:
			intents_and_answers[intent].append(answer)
			intents_and_answers[intent] = list(set(intents_and_answers[intent]))

		with open(answers_filepath, 'w', encoding='utf-8') as json_file:
			json.dump(intents_and_answers, json_file)
			print(f'[INFO] -> Successfully added {answer} to {intent}')


	def add_func(self):
		funcs_filepath = self.INTENTS_FILEPATH + '/intents_and_funcs.json'

		intent = input(Fore.RED + '[ADMIN INPUT] Enter intent ->')
		func = input(Fore.RED + '[ADMIN INPUT] Enter answer ->')

		with open(funcs_filepath, 'r', encoding='utf-8') as json_file:
			intents_and_funcs = json.loads(json_file.read())

		if intent in intents_and_funcs:
			intents_and_funcs[intent].append(func)
			intents_and_funcs[intent] = list(set(intents_and_funcs[intent]))

		with open(funcs_filepath, 'w', encoding='utf-8') as json_file:
			json.dump(intents_and_funcs, json_file)
			print(f'[INFO] -> Успешно добавил {func} в {intent}')

