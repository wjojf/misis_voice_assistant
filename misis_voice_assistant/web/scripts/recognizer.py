from spider import WebSpider
from random import choice
import json


class Recognizer:

	def __init__(self):
		self.spider = WebSpider()

		self.keywords_filepath = '../assets/key_words.json'

		self.intents_and_funcs = {
			
			'show_schedule': 'self.spider.show_schedule()',
			'show_info': None,
			'show_curriculum': 'self.spider.show_curriculum()',
			'show_weather': None

		}

		self.intents_and_answers = {
			'show_schedule': ['Показываю расписание на неделю...', 'Посмотрите расписание на завтра...',],
			'show_curriculum': ['Показываю учебный план на год...', 'Вот учебный план на год..'],
			'show_weather': ['Показываю погоду на день']
		}

	
	
	def save_unknown_command(self, command):
		
		commands = json.loads(open(self.unknown_commands_filepath, encoding='utf-8').read())
		commands["commands"].append(command)

		with open(self.unknown_commands_filepath,'w', encoding='utf-8') as json_file:
			json.dump(commands, json_file)

	

	def classify_intent(self, command):
		
		def unpack_keywords():
			with open(self.keywords_filepath, encoding='utf-8') as json_file:
				return json.loads(json_file.read())

		keywords = unpack_keywords()

		#check for common words
		for intent in keywords:
			for keyword in keywords[intent]:
				if keyword in command:
					return intent

		#TODO: classify intent if none of the keywords are present
		self.save_unknown_command(command)
		return 'Error'



	def answer(self, command):

		intent = self.classify_intent(command)

		if intent in self.intents_and_funcs:
			print(choice(self.intents_and_answers[intent]))
			eval(self.intents_and_funcs[intent])

		else:
			print('Я вас не понимаю...')


