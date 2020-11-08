from matcher import Matcher
import logging

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()

def test_matcher():
	matcher = Matcher()
	embedding = matcher.compute_embedding("Hello world")
	similarity = matcher.compute_similarity(
		embedding,
		matcher.compute_embedding("Hello world")
	)
	
	if round(similarity, 6) != 1:
		raise Exception(f"Same sentences emebddings should have a similarity of 1, got {similarity}")
	
	logger.info("Matcher test passed")

def run_all_tests():
	test_matcher()


if __name__ == "__main__":
	run_all_tests()