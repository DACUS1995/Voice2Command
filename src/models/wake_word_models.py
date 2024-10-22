import torch
import torch.nn as nn
import torch.nn.functional as F

class WakeWordCNNModel_5sec(nn.Module):
	def __init__(self, output_size, training = True):
		super().__init__()
		self.training = training

		self.conv11 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=4, padding=4)
		self.conv12 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=4, padding=4)

		self.conv21 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=4, padding=4)
		self.conv22 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=4, padding=4)

		self.l1 = nn.Linear(11904, 256)
		self.l2 = nn.Linear(256, output_size)

	def forward(self, input):
		out = self.conv11(input)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv12(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv21(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv22(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		# print(out.shape)
		out = out.view(out.size(0), -1)

		out = self.l1(out)
		out = F.leaky_relu(out)

		out = self.l2(out)
		out = F.sigmoid(out)

		return out


class WakeWordCNNModel_3sec(nn.Module):
	def __init__(self, output_size, training = True):
		super().__init__()
		self.training = training

		self.conv11 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=4, padding=4)
		self.conv12 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=4, padding=4)


		self.l1 = nn.Linear(7680, 256)
		self.l2 = nn.Linear(256, output_size)

	def forward(self, input):
		out = self.conv11(input)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv12(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv21(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		out = self.conv22(out)
		out = F.leaky_relu(out)
		out = F.max_pool2d(out, kernel_size=2)
		out = F.dropout(out, 0.1, self.training)

		# print(out.shape)
		out = out.view(out.size(0), -1)

		out = self.l1(out)
		out = F.leaky_relu(out)

		out = self.l2(out)
		out = F.sigmoid(out)

		return out


class WakeWordCNNModel_3sec_2(nn.Module):
	def __init__(self, output_size, training = True):
		super().__init__()
		self.training = training

		self.conv_block1 = nn.Sequential(
			nn.Conv2d(in_channels=1, out_channels=16, kernel_size=2, padding=4),
			nn.MaxPool2d(kernel_size=2),
			nn.BatchNorm2d(16),
			nn.LeakyReLU(0.2, inplace=True),

			nn.Conv2d(in_channels=16, out_channels=16, kernel_size=4, padding=4),
			nn.MaxPool2d(kernel_size=2),
			nn.BatchNorm2d(16),
			nn.LeakyReLU(0.2, inplace=True)
		)
		
		self.conv_block2 = nn.Sequential(
			nn.Conv2d(in_channels=16, out_channels=32, kernel_size=4, padding=4),
			nn.MaxPool2d(kernel_size=2),
			nn.BatchNorm2d(32),
			nn.LeakyReLU(0.2, inplace=True),

			nn.Conv2d(in_channels=32, out_channels=32, kernel_size=4, padding=4),
			nn.MaxPool2d(kernel_size=4),
			nn.BatchNorm2d(32),
			nn.LeakyReLU(0.2, inplace=True)
		)

		self.dropout1 = nn.Dropout(0.6)
		self.dropout2 = nn.Dropout(0.5)

		self.l1 = nn.Linear(6528, 256)
		self.l2 = nn.Linear(256, output_size)

	def forward(self, input):
		out = self.conv_block1(input)
		out = self.conv_block2(out)

		# print(out.shape)
		out = out.view(out.size(0), -1)
		out = self.dropout1(out)

		out = self.l1(out)
		out = F.leaky_relu(out)
		out = self.dropout2(out)

		out = self.l2(out)
		out = F.sigmoid(out)

		return out