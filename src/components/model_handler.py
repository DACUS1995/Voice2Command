import torch
from models import wake_word_models

class ModelHandler():
	def __init__(self):
		self.model = wake_word_models.WakeWordCNNModel(output_size=1)
		self.model.load_state_dict(torch.load("../models/WakeWordCNNModel.pt"))
		self.model.eval()

	def classify(self):
		pass

	def preprocess(self):
		pass