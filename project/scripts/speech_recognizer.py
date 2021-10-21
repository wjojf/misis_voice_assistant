from colorama import init, Fore, Back, Style
import speech_recognition as sr
import pyttsx3

init(autoreset=True)
class SpeechRecognizer:

	def __init__(self):
		self.listener = sr.Recognizer()
		self.engine = pyttsx3.init()
		self.engine.runAndWait()


	def take_command(self):
		'''
		Take voice command using microphone or saying 'Error' 
		:return: command: str
		'''
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
		print(Fore.YELLOW + '[ANSWER] {}'.format(command))
		self.engine.say(command)
