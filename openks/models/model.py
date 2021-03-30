# Copyright (c) 2021 OpenKS Authors, DCD Research Lab, Zhejiang University. 
# All Rights Reserved.

"""
An abstract class for openks models to be trained with Paddle
"""
import logging
from typing import Tuple, List, Any
import torch
import torch.nn as nn
from torch.utils import data
import paddle.fluid as fluid
from paddle.fluid import Variable
from ..common.register import Register
from ..abstract.mtg import MTG
from ..abstract.mmd import MMD

logger = logging.getLogger(__name__)


class PaddleModel(Register):
	def __init__(self, **kwargs):
		self.forward()

	def forward(self, *args):
		return NotImplemented

	def train_forward(self, *args):
		return NotImplemented

	def test_forward(self, *args):
		return NotImplemented

	def backward(self, loss, opt):
		return NotImplemented

	def loss(self, *args):
		return NotImplemented

	@staticmethod
	def _algorithm(*args):
		return NotImplemented



class TorchModel(nn.Module, Register):
	def __init__(self, **kwargs):
		super(TorchModel, self).__init__()

	def forward(self, *args):
		return NotImplemented

	def loss(self, *args):
		return NotImplemented

	def predict(self, *args):
		return NotImplemented

	def _algorithm(self, *args):
		return NotImplemented

	# getter and setter for Ray distributed training
	def get_weights(self):
		return {k: v.cpu() for k, v in self.state_dict().items()}

	def set_weights(self, weights):
		self.load_state_dict(weights)

	def get_gradients(self):
		grads = []
		for p in self.parameters():
			grad = None if p.grad is None else p.grad.data.cpu().numpy()
			grads.append(grad)
		return grads

	def set_gradients(self, gradients):
		for g, p in zip(gradients, self.parameters()):
			if g is not None:
				p.grad = torch.from_numpy(g)


class TorchDataset(data.Dataset):
	def __init__(self, samples):
		self.samples = samples

	def __len__(self):
		return len(self.samples)

	def __getitem__(self, index):
		item = self.samples[index]
		return item


class TFModel(Register):
	def __init__(self, **kwargs):
		return NotImplemented


class MLModel(Register):
	def __init__(self, **kwargs):
		self.process()

	def process(self, *args):
		return NotImplemented


class OpenKSModel(Register):
	def __init__(self):
		pass


class KGLearnModel(OpenKSModel):
	''' Base class for knowledge graph representation learning trainer '''
	def __init__(self, name: str = 'model-name', graph: MTG = None, args: List = None):
		self.name = name
		self.graph = graph

	def parse_args(self):
		return NotImplemented

	def triples_reader(self, *args):
		return NotImplemented

	def triples_generator(self, *args):
		return NotImplemented

	def evaluate(self, *args):
		return NotImplemented

	def load_model(self, *args):
		return NotImplemented

	def save_model(self, *args):
		return NotImplemented

	def run(self, *args):
		return NotImplemented


class GeneralModel(OpenKSModel):
	''' Base class for knowledge graph building trainer, such as text and image information extraction '''
	def __init__(self, name: str = 'model-name', dataset: MMD = None, args: List = None):
		self.name = name
		self.dataset = dataset

	def parse_args(self):
		return NotImplemented

	def data_reader(self, *args):
		return NotImplemented

	def evaluate(self, *args):
		return NotImplemented

	def load_model(self, *args):
		return NotImplemented

	def save_model(self, *args):
		return NotImplemented

	def run(self, *args):
		return NotImplemented


class RecModel(OpenKSModel):
	''' Base class for recommendation trainer, such as text and image information extraction '''
	def __init__(self, name: str = 'model-name', dataset: MMD = None, args: List = None):
		self.name = name
		self.dataset = dataset

	def parse_args(self):
		return NotImplemented

	def data_reader(self, *args):
		return NotImplemented

	def evaluate(self, *args):
		return NotImplemented

	def load_model(self, *args):
		return NotImplemented

	def save_model(self, *args):
		return NotImplemented

	def run(self, *args):
		return NotImplemented
