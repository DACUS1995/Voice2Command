from .simple_commands import SimpleCommand
import logging

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()

def test_simple_command():
	output = SimpleCommand.run({
		"command": "echo Hello World"
	})
	assert output == "Hello World"
	logger.info("SimpleCommand test passed")

def run_all_tests():
	test_simple_command()


if __name__ == "__main__":
	run_all_tests()