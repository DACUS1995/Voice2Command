import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


class Listener():
	def __init__(self, file = None):
		self.p = pyaudio.PyAudio()
		
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

	def process(self):
		pass

	def start(self):
		self.running = True

		while self.running:
			frames = []
			for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.readframes(CHUNK)
				frames.append(data)

			

	def stop(self):
		self.running = False
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()