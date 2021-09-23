import json
commands = json.loads(open('../assets/intents_json/intents_and_answers.json', encoding='utf-8').read())

with open('../assets/intents_json/intents_and_answers.json', 'w') as json_file:
    json.dump(commands, json_file, ensure_ascii=False)