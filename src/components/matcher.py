import json
import numpy as np
from sentence_transformers import SentenceTransformer


class Matcher():
	def __init__(self):
		self.commands_config = self.load_commands_config()
		self.model = SentenceTransformer('bert-base-nli-mean-tokens')
		self.commands_embeddings = []

		# precompute the embeddings
		for idx, command_config in enumerate(self.commands_config):
			embedding = self.compute_embedding(command_config["sentence"])
			self.commands_embeddings.append(embedding)



	def load_commands_config(self, path="commands_config.json"):
		with open(path) as json_file:
			commands_config = json.load(json_file)
			return commands_config


	def compute_embedding(self, sentence):
		# TODO Check the improvements of using a batch of sentences
		sentence_embedding = self.model.encode([sentence])[0]
		return sentence_embedding


	def find_match(self, sentence):
		embedding = self.compute_embedding(sentence)
		best_similarity = 0
		best_match_idx = None

		# The order of the commands config should be the same as the embeddings
		for idx, command_config in enumerate(self.commands_config):
			similarity = self.compute_similarity(embedding, self.commands_embeddings[idx])
			
			if similarity > best_similarity:
				best_similarity = similarity
				best_match_idx = idx

		assert best_match_idx is not None
		return self.commands_config[idx]


	def compute_similarity(self, embedding_one, embedding_two):
		if not isinstance(embedding_one, np.ndarray) or not isinstance(embedding_two, np.ndarray):
			raise Exception("Embeddings must be np.ndarray")

		if len(embedding_one) != len(embedding_two):
			raise Exception("Embeddings have different sizes")

		cos_sim = np.dot(embedding_one, embedding_two) / (np.linalg.norm(embedding_one) * np.linalg.norm(embedding_two))
		return cos_sim