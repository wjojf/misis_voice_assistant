from colorama import init, Fore, Back, Style
import speech_recognition as sr
import pyttsx3

init(autoreset=True)
class SpeechRecognizer:

	def __init__(self):
		self.listener = sr.Recognizer()
		try:
			self.engine = pyttsx3.init()
		except Exception as error:
			print(error)


	def take_command(self):
		'''
		Take voice command using microphone or saying 'Error' 
		:return: command: str
		'''
		try:
			with sr.Microphone() as source:
				print(Fore.YELLOW + 'Cлушаю команду...')
				voice = self.listener.listen(source,10,3)
				command = self.listener.recognize_google(voice, language='ru-RU')
				
				if command != '':
					return command.lower()
				
				return 'error'
		except:
			return 'error'

	def is_valid(self, command):
		return command != 'error'

	def say(self, command):
		print(Fore.YELLOW + '[Леонид] {}'.format(command))
		self.engine.say(command)
		self.engine.runAndWait()
