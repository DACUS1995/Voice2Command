import argparse
import logging
import threading
import time

from components.listener import Listener
from components.wake_model_handler import ModelHandler as WakeModelHandler
from components.processor import Processor
from components.speech_handler import SpeechHandler

log_format = "%(asctime)s [%(module)s] : %(message)s"
logging.basicConfig(level="DEBUG", format=log_format)
logger = logging.getLogger()


def start_service(file_path = None):
	logger.info("Starting Voice2Command service")
	started_threads = []

	listener = None
	if file_path is not None:
		listener = Listener("true_sample.wav")
	else:
		listener = Listener()

	wake_model_handler = WakeModelHandler()
	speech_handler = SpeechHandler()
	processor = Processor(
		listener, 
		wake_model_handler, 
		speech_handler
	)

	run_event = threading.Event()
	run_event.set()

	started_threads.append(processor.run(run_event))
	started_threads.append(listener.run(run_event))

	try:
		while 1:
			time.sleep(1)
	except KeyboardInterrupt:
		logger.info(f"Attempting to close {len(started_threads)} threads.")
		run_event.clear()
		for thread in started_threads:
			if thread.is_alive():
				thread.join()
		logger.info("Threads successfully closed")



def main(args):
	if args.debug_mode_enabled:
		start_service("true_sample.wav")
	else:
		start_service()
	# threading.Event().wait()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument("--method", type=str, default="orb")
	# parser.add_argument("--directory", type=str, default="./images/noisy_images")
	# parser.add_argument("--scale-percent", type=int, default=200)
	parser.add_argument("--debug-mode-enabled", default=False, action="store_true")
	args = parser.parse_args()
	main(args)
