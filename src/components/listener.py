import pyaudio
import wave
import threading
import queue
import logging

logger = logging.getLogger()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


class Listener():
	def __init__(self, file = None):
		self.p = pyaudio.PyAudio()
		self.q = queue.Queue()

		if file is None:
			self.stream = self.p.open(
				format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK
			)
		else:
			self.stream = wave.open(file)
			
		self.running = False

	def run(self):
		thread = threading.Thread(target=self.start, daemon=True)
		thread.start()

	def start(self):
		self.running = True
		logger.info(f"Starting {self.__class__.__name__}")

		while self.running:
			frames = []
			for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.readframes(CHUNK)
				frames.append(data)

			self.q.put(frames)
			print(f"{self.__class__.__name__}")

			

	def stop(self):
		self.running = False
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()