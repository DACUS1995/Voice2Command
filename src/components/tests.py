from matcher import Matcher
import logging

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()

def test_matcher():
	matcher = Matcher()

def run_all_tests():
	test_matcher()


if __name__ == "__main__":
	run_all_tests()