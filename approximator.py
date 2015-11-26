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
	def getY(self, inpt):
		raise NotImplementedError("Must override getY")

	@abstractmethod
	def update(self, state, action, reward, new_state, new_action):
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
		q_old = self.qvalue(state, action)
		q_new = self.qvalue(new_state, new_action)
		target = q_old + self.alpha*(reward + (self.gamma*q_new)-q_old)
		

		self.ds.addSample(inpt, target)
		# print inpt.shape, target.shape
		# print inpt, target
		trainer = BackpropTrainer(self.net, self.ds)
		# try:
		# 	trainer.trainUntilConvergence()
		# except:
		trainer.train()

class GradientDescent(FunctionApproximator):
	#this is linear function: http://www.cc.gatech.edu/~mnelson/darcs/rl/_darcs/current/src/LinearStateActionValueFunc.java
	#
	def __init__(self, num_features, alpha):
		super(GradientDescent,self).__init__(num_features)
		self.params = np.ones(num_features)
		self.alpha = alpha

	def getY(self, X):
		return np.dot(self.basis_f(X),self.params)

	def update(self, delta, eligibility):
		self.params = self.params + self.alpha*delta*eligibility

	def gradient(self, inpt):
		#for linear function
		return inpt

	def basis_f(self, x):
		return x


if __name__=='__main__':
	g = GradientDescent(300)
	g.getY(np.ones(300))