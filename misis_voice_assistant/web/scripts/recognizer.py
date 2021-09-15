from spider import WebSpider
from random import choice
import json


class Recognizer:

	def __init__(self):
		
		self.intents_and_keywords_filepath = '../assets/intents_json/intents_and_keywords.json'
		self.intents_and_funcs_filepath = '../assets/intents_json/intents_and_funcs.json'
		self.intents_and_answers_filepath = '../assets/intents_json/intents_and_answers.json'

		self.intents_and_funcs = json.loads(open(self.intents_and_funcs_filepath).read())
		self.intents_and_answers = json.loads(open(self.intents_and_answers_filepath).read())
		self.intents_and_keywords = json.loads(open(self.intents_and_keywords_filepath).read())
		
		self.unknown_commands_filepath = '../assets./errors/unknown_commands.json'
	
	
	def save_unknown_command(self, command):
		
		commands = json.loads(open(self.unknown_commands_filepath, encoding='utf-8').read())
		commands["commands"].append(command)

		with open(self.unknown_commands_filepath,'w', encoding='utf-8') as json_file:
			json.dump(commands, json_file)

	
	def classify_intent(self, command):
		command = command.lower()

		#check for common words
		for intent in self.intents_and_keywords:
			for keyword in self.intents_and_keywords[intent]:
				if keyword in command:
					return intent

		
		#TODO: classify intent if none of the keywords are present
		self.save_unknown_command(command)
		return 'error'


	def get_func(self, command):
		print(f'Поступившая команда: {command}')

		intent = self.classify_intent(command)

		if intent in self.intents_and_funcs:
			return {
					 'func': self.intents_and_funcs[intent],
					 'answer': choice(self.intents_and_answers[intent])
					}
		else:
			return {'func': None, 'answer': 'Я вас не понял...'}
