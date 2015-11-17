import cPickle
import math
import random
import sys
import numpy as np
import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

filename = 'pickle_fst.pkl'
class NNSarsa:
	def __init__(self, state_dim, action_dim, e=0.3, alpha=0.75, gamma=0.9, trained=filename):
		self.actions = list(range(action_dim))
		self.state_dim = state_dim

		self.e = e
		self.alpha = alpha
		self.gamma = gamma

		self.num_input_neurons = state_dim*4 + action_dim
		num_hidden_neurons = 100
		num_output_neurons = 1

		try:
			self.net = cPickle.load(open(trained))
		except IOError, e:
			print 'trained file not found'
			self.net = buildNetwork(self.num_input_neurons, num_hidden_neurons, num_output_neurons, bias=True)

	def e_greedy(self, state):
		"""
		make e decreasing, as e(t) = e(0)/(1+t*dr)  ; dr is decreasing rate of e
		"""
		# Explore
		if random.random() < self.e:
			action = random.randint(0, len(self.actions)-1)
			explore = True
		# Exploit
		else:
			explore = False
			for index in range(len(self.actions)):
				cur_value = self.qvalue(state, index)
				
				if index==0:
					max_value = cur_value
					max_action = 0
					
				elif cur_value>max_value:
					max_value = cur_value
					max_action = index
			action = max_action
		return action

	def sa_to_input(self, state, action):
		"""
		action is int
		"""
		actions_vec = np.zeros(len(self.actions), dtype=np.int)
		actions_vec[action] = 1
		
		#s,a pair
		net_input = np.concatenate([state.get_vec(), actions_vec])
		return net_input

	def qvalue(self, state, action):
		#q value for s,a
		cur_value = self.net.activate(self.sa_to_input(state, action))
		return cur_value

	def act(self, state):
		
		"""
		have to change initial value ?
		or use boltzmann exploration: refer solar boat thesis paper
		"""

		action = self.e_greedy(state)
		return action
		#call update after act

	def update_q(self, state, action, reward, new_state, new_action):
		# if not state:
		# 	return

		q_old = self.qvalue(state, action)
		q_new = self.qvalue(new_state, new_action)
		
		target = q_old + self.alpha*(reward + (self.gamma*q_new)-q_old)

		ds = SupervisedDataSet(self.num_input_neurons, 1)
		ds.addSample(self.sa_to_input(state, action), np.array([target]))
		trainer = BackpropTrainer(self.net, ds)
		trainer.trainUntilConvergence()

		# print 'old: ', q_old
		# print 'new: ', self.qvalue(state, action)
		#until convergence?
	def save_nnet(self):
		fp = open(filename, "w")
		cPickle.dump(self.net, fp)
		fp.close()
