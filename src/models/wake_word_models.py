import torch
import torch.nn as nn
import torch.nn.functional as F

class WakeWordCNNModel(nn.Module):
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