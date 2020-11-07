import json

class Matcher():
	def __init__(self):
		commands_config = self.load_commands_config()
		print(commands_config[0])

	def load_commands_config(self):
		with open("../commands_config.json") as json_file:
			commands_config = json.load(json_file)
			return commands_config