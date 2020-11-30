import logging
import threading
import time
import numpy as np
import winsound
import speech_recognition as sr

import commands
from .matcher import Matcher

logger = logging.getLogger()

class Processor():
	def __init__(self, listener, wake_model_handler, speech_handler):
		self.listener = listener
		self.wake_model_handler = wake_model_handler
		self.speech_handler = speech_handler
		self.matcher = Matcher()

		self._skip_next = False


	def start(self, run_event):
		logger.info(f"Starting {self.__class__.__name__}")

		while run_event.is_set():
			if self._skip_next:
				self.listener.q.get()
				self.listener.q.task_done()
				self._skip_next = False
				logger.info("Skipping the next wake frames")
				time.sleep(3)
				continue

			if not self.listener.q.empty():
				frames = self.listener.q.get()
				data = np.hstack(frames)
				self.process_wake_data(data)
				self.listener.q.task_done()
			time.sleep(0.25)
			logger.info(f"Queue is empty {self.listener.q.empty()}")


	def process_wake_data(self, data):
		logger.info("Processing data")
		wake_word_preds = self.wake_model_handler.classify(data)
		
		print(wake_word_preds)
		if wake_word_preds[0][0] == 1:
			print("Waking up!")
			self._skip_next = True
			self.notify_waking()

			try:
				audio_data = self.speech_handler.capture_audio_command()
				transcription = self.speech_handler.transcribe(audio_data)
				self.process_transcription_data(transcription)
				print(transcription)
			except sr.WaitTimeoutError:
				pass


	def process_transcription_data(transcription):
		command = self.find_command_match(transcription)
		self.run_command(command)


	def find_command_match(self, transcription):
		command = self.matcher.find_match(transcription)
		return command


	def run_command(self, command):
		if command["type"] == commands.SIMPLE_COMMAND_TYPE:
			output = commands.SimpleCommand.run(command)
			return output

		raise Exception(f"Unhandled command type {command['type']}")


	def run(self, run_event):
		thread = threading.Thread(target=self.start, args=(run_event,), daemon=True)
		thread.start()
		return thread


	def notify_waking(self):
		winsound.Beep(
			frequency=500, 
			duration=400
		)