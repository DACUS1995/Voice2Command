import speech_recognition as sr
import winsound

from config import Config

class SpeechHandler:
	def __init__(self):
		self.recognizer = sr.Recognizer()
		self.mic = sr.Microphone()

	def capture_audio_command(self, file_path = None):
		audio_data = None
		if file_path is None:
			with self.mic as source:
				self.recognizer.adjust_for_ambient_noise(source)
				audio_data = self.recognizer.listen(source, timeout = Config.COMMAND_TIMEOUT)
		else:
			audio_handler = sr.AudioFile(file_path)
			with audio_handler as source:
				audio_data = self.recognizer.record(source)

		assert audio_data is not None
		return audio_data

	def transcribe(self, audio_data):
		# transcription = self.recognizer.recognize_sphinx(audio_data)
		transcription = self.recognizer.recognize_google(audio_data)
		return transcription