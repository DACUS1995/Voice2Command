import argparse
import logging
import threading
import time

from components.listener import Listener
from components.model_handler import ModelHandler
from components.processor import Processor

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()


def start_service():
	logger.info("Starting Voice2Command service")

	listener = Listener("true_sample.wav")
	model_handler = ModelHandler()
	processor = Processor(listener, model_handler)

	run_event = threading.Event()
	run_event.set()
	thread = processor.run(run_event)

	try:
		while 1:
			time.sleep(1)
			print("Waiting")
	except KeyboardInterrupt:
		print("attempting to close threads.")
		run_event.clear()
		thread.join()
		print("threads successfully closed")



def main(args):
	start_service()
	# threading.Event().wait()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument("--method", type=str, default="orb")
	# parser.add_argument("--directory", type=str, default="./images/noisy_images")
	# parser.add_argument("--scale-percent", type=int, default=200)
	# parser.add_argument("--draw-matches", default=False, action="store_true")
	args = parser.parse_args()
	main(args)
