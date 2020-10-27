import speech_recognition as sr	

class SpeechHandler:
	def __init__(self):
		self.recognizer = sr.Recognizer()

	def transcribe(self, audio_data = None):
		r = sr.Recognizer()
		audio_handler = sr.AudioFile("speech.wav")
		with audio_handler as source:
			audio_data = r.record(source)
			# transcription = self.recognizer.recognize_sphinx(audio_data)
			transcription = self.recognizer.recognize_google(audio_data)
			return transcription