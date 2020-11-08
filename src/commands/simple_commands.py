import subprocess


class CommandBase():
	@staticmethod
	def run(args):
		raise NotImplementedError


class SimpleCommand(CommandBase):
	def __init__(self):
		pass

	@staticmethod
	def run(args):
		command = args["command"]
		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		output, err = process.communicate()
		process.wait()
		return output.decode('utf-8').strip()
