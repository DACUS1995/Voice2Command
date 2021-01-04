import numpy as np
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
import pathlib
import random
import torch
import torch.nn as nn
from torch.utils.data import DataLoader


from models import wake_word_models
from training.dataset import CustomDataset as Dataset

np.random.seed(0)


def train(
	model,
	optimizer,
	loss_criterion,
	training_dataset,
	validation_dataset,
	num_epochs
	) -> nn.Module: 

	EARLY_STOPPING_PATIENCE = 3
	previous_epoch_loss = None
	early_stopping_counter = 0

	scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

	training_dataloader = DataLoader(training_dataset, batch_size=5, shuffle=True)
	testing_dataloader = DataLoader(validation_dataset)

	training_dataset_size = len(training_dataset)
	validation_dataset_size = len(validation_dataset)
	
	device = torch.device("cuda")
	model.to(device)

	for epoch in range(num_epochs):
		print('Epoch {}/{}'.format(epoch, num_epochs))
		print('-' * 10)

		##### TRAINING ######
		model = model.train()
		training_loss = []
		running_loss = 0.0
		running_corrects = 0


		# for i, data in enumerate(tqdm(training_dataloader, desc=f"Epoch | training [{epoch + 1}] progress")):
		for i, data in enumerate(training_dataloader):
			x_batch, label_batch = data
			x_batch, label_batch = x_batch.to(device), label_batch.to(device)

			optimizer.zero_grad()
			outputs = model(x_batch)

			loss = loss_criterion(outputs, label_batch)

			loss.backward()
			optimizer.step()

			# statistics
			preds =  torch.round(outputs)
			running_loss += loss.item() * x_batch.size(0)
			running_corrects += torch.sum(preds == label_batch.detach())
			training_loss.append(loss.item())


		epoch_loss = running_loss / training_dataset_size
		epoch_acc = running_corrects.double() / training_dataset_size
		print('Training step => Loss: {:.4f} Acc: {:.4f}'.format(
			epoch_loss, epoch_acc
		))

		scheduler.step(epoch_acc)

		###### VALIDATION ######
		model = model.eval()
		running_loss = 0.0
		running_corrects = 0

		for i, data in enumerate(testing_dataloader):
			with torch.no_grad():
				x_batch, label_batch = data
				x_batch, label_batch = x_batch.to(device), label_batch.to(device)

				outputs = model(x_batch)
				loss = loss_criterion(outputs, label_batch)

				# statistics
				preds =  torch.round(outputs)
				running_loss += loss.item() * x_batch.size(0)
				running_corrects += torch.sum(preds == label_batch.detach())


		epoch_testing_loss = running_loss / validation_dataset_size
		epoch_testing_acc = running_corrects.double() / validation_dataset_size
		print('Testing step => Loss: {:.4f} Acc: {:.4f} \n'.format(
			epoch_testing_loss, epoch_testing_acc
		))

		if previous_epoch_loss is None:
			previous_epoch_loss = epoch_loss
		else:
			if epoch_loss > previous_epoch_loss:
				early_stopping_counter += 1
				previous_epoch_loss = epoch_loss
			else:
				early_stopping_counter = 0

		if early_stopping_counter == EARLY_STOPPING_PATIENCE:
			break
		
	return model


def main(args):
	model = wake_word_models.WakeWordCNNModel_3sec_2(output_size=1)
	optimizer = torch.optim.AdamW(model.parameters(), lr=0.0001, betas=(0.9, 0.999), eps=1e-08, weight_decay=1e-4)
	loss_criterion = torch.nn.BCELoss(size_average = True)
	num_epochs = 70

	training_dataset = Dataset(
		wake_words_root_path = args.wake_words_path,
		background_sounds_root_path = args.background_noise_path
	)
	validation_dataset = Dataset(
		wake_words_root_path = "D:/Workspace/Projects/Voice2Command/recordings/test",
		background_sounds_root_path = "D:/Storage/UrbanSound8K/audio/fold2",
		testing=True
	)

	trained_model = train(
		model,
		optimizer,
		loss_criterion,
		training_dataset,
		validation_dataset,
		num_epochs
	)

	torch.save(trained_model.state_dict(), f"model.pt")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	# The recordings root directory should have two folders with positive and negative samples
	parser.add_argument("--wake-words-path", type=str, default="D:/Workspace/Projects/Voice2Command/recordings")
	parser.add_argument("--background-noise-path", type=str, default="D:/Storage/UrbanSound8K/audio/fold1")
	args = parser.parse_args()
	main(args)
