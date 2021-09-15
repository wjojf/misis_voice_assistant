import speech_recognition as sr
import pyttsx3


class SpeechRecognizer:

	def __init__(self):
		self.listener = sr.Recognizer()
		self.engine = pyttsx3.init()


	def take_command(self):
		try:
			with sr.Microphone() as source:
				print('[INFO] -> Listening...')
				voice = self.listener.listen(source)
				command = self.listener.recognize_google(voice, language='ru-RU')

				return command.lower()
		except:
			return 'ошибка!'

	def is_valid(self, command):
		return command != 'ошибка!'

	def say(self, command):
		self.engine.say(command)
