import pyaudio
import wave
import threading
import queue
import logging
import time
import librosa
import numpy as np

from config import Config

logger = logging.getLogger()

CHUNK = 1024
# FORMAT = pyaudio.paFloat32
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2


class Listener():
	def __init__(self, file_path = None):
		self.running = False
		self.p = pyaudio.PyAudio()
		self.q = queue.Queue()
		self.file_path = file_path
		self.mic_stream = None
		self.file_stream = None

		if file_path is None:
			self.mic_stream = self.p.open(
				format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK
			)
		else:
			pass
			# self.file_stream = wave.open(file)
			

	def run(self, run_event):
		thread = threading.Thread(target=self.start, args=(run_event,) ,daemon=True)
		thread.start()
		return thread

	def start(self, run_event):
		self.running = True
		logger.info(f"Starting {self.__class__.__name__}")
		
		if self.mic_stream is None:
			y, sr = librosa.core.load(self.file_path, Config.RATE)
			self.q.put(y)
			return
		else:
			while run_event.is_set():
				frames = []
				frames_save = []

				for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
					data = self.mic_stream.read(CHUNK)
					# logger.info(f"Read {len(data)} bytes")
					frames_save.append(data)
					frames.append(np.fromstring(data, dtype=np.int16).astype(np.float32))

				print("#############################")
				self.q.put(frames)
				self.save_recording(frames_save)
				time.sleep(0.5)

	def save_recording(self, frames):
		waveFile = wave.open("new_recording.wav", 'wb')
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(self.p.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()
			

	def stop(self):
		self.running = False
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()