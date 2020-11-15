import torch
import numpy as np
import librosa
import logging

from models import wake_word_models
from config import Config

logger = logging.getLogger()

class ModelHandler():
	def __init__(self):
		self.model = wake_word_models.WakeWordCNNModel(output_size=1)
		self.model.load_state_dict(torch.load("../models/WakeWordCNNModel_3sec.pt"))
		self.model.eval()
		logger.info("Model loaded")

	def classify(self, data):
		#TODO make batch processing
		data = self.preprocess(data)
		data = data.unsqueeze(dim=0)
		
		with torch.no_grad():
			output = self.model(data)
			return output.cpu().detach().numpy()

	def preprocess(self, data):
		if not isinstance(data, np.ndarray):
			raise Exception("Data must be a numpy array")

		sample_size = Config.RATE * Config.RECORD_SECONDS

		if len(data) < sample_size:
			data = np.pad(data, (0, sample_size - len(data)))
		else:
			data = data[:sample_size]

		S = librosa.feature.melspectrogram(y=data, sr=Config.RATE)
		S_db = librosa.core.power_to_db(S)
		data = torch.from_numpy(S_db).unsqueeze(dim=0).float()

		return data