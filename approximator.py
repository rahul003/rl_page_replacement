from abc import abstractmethod
import numpy as np
import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer
from pybrain.structure import FullConnection

class FunctionApproximator(object):
	def __init__(self,num_features):
		self.num_dim = num_features

	@abstractmethod
	def getY(self, input):
		raise NotImplementedError("Must override getY")

	@abstractmethod
	def update(self, input, target):
		raise NotImplementedError("Must override update")


class NNet(FunctionApproximator):
	def __init__(self, num_features, num_hidden_neurons):
		super(NNet,self).__init__(num_features)

		self.ds = SupervisedDataSet(num_features, 1)

		self.net = FeedForwardNetwork()
		self.net.addInputModule(LinearLayer(num_features, name='in'))
		self.net.addModule(LinearLayer(num_hidden_neurons, name='hidden'))
		self.net.addOutputModule(LinearLayer(1, name='out'))
		self.net.addConnection(FullConnection(self.net['in'], self.net['hidden'], name='c1'))
		self.net.addConnection(FullConnection(self.net['hidden'], self.net['out'], name='c2'))
		self.net.sortModules()

	def getY(self, inpt):
		#giving NAN
		return self.net.activate(inpt)

	def update(self, inpt, target):
		self.ds.addSample(inpt, target)
		# print inpt.shape, target.shape
		# print inpt, target
		trainer = BackpropTrainer(self.net, self.ds)
		# try:
		# 	trainer.trainUntilConvergence()
		# except:
		trainer.train()

class GradientDescent(FunctionApproximator):
	def __init__(self, num_features):
		super(GradientDescent,self).__init__(num_features)
		self.params = np.ones(num_features)

	def getY(self, X):
		return np.dot(X,self.params)

	def update(self, inpt, target):
		


if __name__=='__main__':
	g = GradientDescent(300)
	g.getY(np.ones(300))