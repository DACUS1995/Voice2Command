import logging
import threading
import time

logger = logging.getLogger()

class Processor():
	def __init__(self, listener, model_handler, speech_handler):
		self.listener = listener
		self.model_handler = model_handler
		self.speech_handler = speech_handler

	def start(self, run_event):
		logger.info(f"Starting {self.__class__.__name__}")

		while run_event.is_set():
			if not self.listener.q.empty():
				data = self.listener.q.get()
				self.process_wake_data(data)
				self.listener.q.task_done()
			time.sleep(0.5)
			logger.info(f"Queue is empty {self.listener.q.empty()}")

	def process_wake_data(self, data):
		logger.info("Processing data")
		wake_word_preds = self.model_handler.classify(data)
		
		if wake_word_preds[0][0] == 1:
			print("Waking up!")
			audio_data = self.speech_handler.capture_audio_command("speech.wav")
			transcription = self.speech_handler.transcribe()
			print(transcription)

	def process_transcription_data(transcription):
		# TODO Choose the good command based on the transcription
		pass

	def run(self, run_event):
		thread = threading.Thread(target=self.start, args=(run_event,), daemon=True)
		thread.start()
		return thread