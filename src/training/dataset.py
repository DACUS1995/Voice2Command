import librosa
import librosa.display
import soundfile as sf
import pathlib
import random
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
from torchaudio import transforms

torch.manual_seed(0)
np.random.seed(0)


class CustomDataset(Dataset):
	def __init__(
		self, 
		wake_words_root_path = "D:/Workspace/Projects/Voice2Command/recordings/positive",
		background_sounds_root_path = "D:/Storage/UrbanSound8K/audio/fold1",
		max_length = 3,
		sampling_rate = 44100, #44.1 Hz
		testing = False
		):
		self.wake_words_positive_root_path = wake_words_root_path + "/positive"
		self.wake_words_negative_root_path = wake_words_root_path + "/negative"
		self.sampling_rate = sampling_rate
		self.background_sounds_root_path = background_sounds_root_path
		
		self.generated_samples = []
		self.sample_size = sampling_rate * max_length

		self.background_noise_sound_paths = list(pathlib.Path(background_sounds_root_path).glob('*.wav'))
		self.wake_words = self._load_wake_words(self.wake_words_positive_root_path)
		self.wake_words_negative = self._load_wake_words(self.wake_words_negative_root_path)

		#Spec Augment transforms
		self.transforms = nn.Sequential(
			transforms.FrequencyMasking(freq_mask_param=2),
			transforms.TimeMasking(time_mask_param=4)
		)

		number_of_samples = 400
		if testing == True:
			number_of_samples = 50

		for idx, path in enumerate(self.background_noise_sound_paths[:number_of_samples]):
			y, sr = librosa.core.load(path, sr=sampling_rate)

			if len(y) < self.sample_size:
				y = np.pad(y, (0, self.sample_size - len(y)))
			else:
				y = y[:self.sample_size]

			y_false = np.array(y, copy=True)
			y_true = y

			#Positive
			wake_word = self.sample_wake_word(self.wake_words)
			interval = self._get_random_time_interval(len(wake_word), max_length * sampling_rate)
			self._overlay_wakeword(y_true[interval[0]:interval[1]], wake_word)
			# self._save_sound(y)

			S_true = librosa.feature.melspectrogram(y=y_true, sr=sr, hop_length=128)
			S_db_true = librosa.core.power_to_db(S_true)
			S_db_true = self.transforms(torch.from_numpy(S_db_true))

			#Negative
			if random.random() > 0.5:
				wake_word = self.sample_wake_word(self.wake_words_negative)
				interval = self._get_random_time_interval(len(wake_word), max_length * sampling_rate)
				self._overlay_wakeword(y_false[interval[0]:interval[1]], wake_word)
				self._save_sound(y_false)
			
			S_false = librosa.feature.melspectrogram(y=y_false, sr=sr, hop_length=128)
			S_db_false = librosa.core.power_to_db(S_false)
			S_db_false = self.transforms(torch.from_numpy(S_db_false))

			# Labels for position detection of the wake word
			# label = np.zeros(sample_size)
			# label[interval[1]:interval[1] + 50] = 1

			self.generated_samples.append(
				(S_db_true.unsqueeze(dim=0).float(), torch.tensor([1]).float())
			)

			self.generated_samples.append(
				(S_db_false.unsqueeze(dim=0).float(), torch.tensor([0]).float())
			)

	def __getitem__(self, idx):
		return self.generated_samples[idx]

	def _get_random_time_interval(self, interval_size, max_size):
		interval_start = np.random.randint(low=0, high=max_size - interval_size)
		interval_end = interval_start + interval_size

		return interval_start, interval_end

	def _overlay_wakeword(self, background, addition):
		background += addition
		background /= 2

	def _save_sound(self, data, name="generated_file.wav"):
		sf.write(name, data, self.sampling_rate)

	def __len__(self):
		return len(self.generated_samples)

	def _load_wake_words(self, wake_words_positive_root_path):
		wake_word_paths = list(pathlib.Path(wake_words_positive_root_path).glob('*.wav'))
		wake_words = []

		for idx, wake_word_path in enumerate(wake_word_paths):
			wake_word, _ = librosa.core.load(wake_word_path, sr=44100)
			
			if len(wake_word) > self.sample_size:
				raise Exception(f"Wake word size {len(wake_word)} bigger than the background noise max length {self.sample_size}")
		
			wake_word = np.pad(wake_word, (0, self.sampling_rate - len(wake_word)))
			wake_words.append(wake_word)

		return wake_words

	def sample_wake_word(self, words):
		return random.choice(words)