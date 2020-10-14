import argparse
import logging

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()


def start_service():
	logger.info("Starting Voice2Command service")

def main(args):
	start_service()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument("--method", type=str, default="orb")
	# parser.add_argument("--directory", type=str, default="./images/noisy_images")
	# parser.add_argument("--scale-percent", type=int, default=200)
	# parser.add_argument("--draw-matches", default=False, action="store_true")
	args = parser.parse_args()
	main(args)
