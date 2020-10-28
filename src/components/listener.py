import pyaudio
import wave
import threading
import queue
import logging
import time
import librosa

from config import Config

logger = logging.getLogger()

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


class Listener():
	def __init__(self, file_path = None):
		self.p = pyaudio.PyAudio()
		self.q = queue.Queue()
		self.file_path = file_path

		if file_path is None:
			self.stream = self.p.open(
				format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK
			)
		else:
			pass
			# self.stream = wave.open(file)
			
		self.running = False

	def run(self, run_event):
		thread = threading.Thread(target=self.start, args=(run_event,) ,daemon=True)
		thread.start()
		return thread

	def start(self, run_event):
		self.running = True
		logger.info(f"Starting {self.__class__.__name__}")
		
		if self.file_path is not None:
			y, sr = librosa.core.load(self.file_path, Config.RATE)
			self.q.put(y)
			return
		else:
			while run_event.is_set():
				frames = []
				for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
					data = self.stream.readframes(CHUNK)
					logger.info(f"Read {len(data)} bytes")
					frames.append(data)

				self.q.put(frames)
				time.sleep(0.5)

			

	def stop(self):
		self.running = False
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()