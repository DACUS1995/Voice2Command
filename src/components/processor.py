import logging
import threading
import time

logger = logging.getLogger()

class Processor():
	def __init__(self, listener, model_handler):
		self.listener = listener
		self.model_handler = model_handler

	def start(self, run_event):
		logger.info(f"Starting {self.__class__.__name__}")

		while run_event.is_set():
			if not self.listener.q.empty():
				data = self.listener.q.get()
				self.process_data(data)
				self.listener.q.task_done()
			time.sleep(0.5)
			logger.info(f"Queue is empty {self.listener.q.empty()}")

	def process_data(self, data):
		logger.info("Processing data")
		print(self.model_handler.classify(data))

	def run(self, run_event):
		thread = threading.Thread(target=self.start, args=(run_event,), daemon=True)
		thread.start()
		return thread