import json

with open("../assets/key_words.json", encoding='utf-8') as json_file:
	keywords = json.loads(json_file.read())


print(keywords)