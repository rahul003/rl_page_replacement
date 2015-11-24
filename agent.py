import cPickle
import math
import random
import sys

import numpy as np

from approximator import NNet

class SarsaApprox:
	def __init__(self, state_dim, action_dim, e=0.3, alpha=0.75, gamma=0.9, trained='pickle_fst.pkl'):
		self.actions = list(range(action_dim))
		self.state_dim = state_dim

		self.e = e
		self.alpha = alpha
		self.gamma = gamma

		self.num_feats = state_dim*3 + action_dim

		try:
			self.approximator = cPickle.load(open(trained))
		except IOError, e:
			print 'trained file not found'
			# self.approximator = GradientDescent(self.num_feats)
			self.approximator = NNet(self.num_feats, 100)

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
			values = []
			for index in range(len(self.actions)):
				cur_value = self.qvalue(state, index)
				if cur_value not in values:
					values.append(cur_value)
				# print cur_value,
				if index==0:
					max_value = cur_value
					max_action = 0
					
				elif cur_value>=max_value:
					max_value = cur_value
					max_action = index
			action = max_action
			# if len(values)>1:
				# print values
			# print 'Max: ',max_action, max_value
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
		cur_value = self.approximator.getY(self.sa_to_input(state, action))
		return cur_value

	def act(self, state):
		"""
		have to change initial value ?
		or use boltzmann exploration: refer solar boat thesis paper
		"""
		action = self.e_greedy(state)
		return action


	def update_q(self, state, action, reward, new_state, new_action):
		q_old = self.qvalue(state, action)
		q_new = self.qvalue(new_state, new_action)
		target = q_old + self.alpha*(reward + (self.gamma*q_new)-q_old)
		# print target
		self.approximator.update(self.sa_to_input(state, action), np.array(target))

	def save_nnet(self):
		fp = open(filename, "w")
		cPickle.dump(self.net, fp)
		fp.close()

	# def save_example(self, inp, outp, old):
	# 	self.q_old[len(self.ds)] = old
	# 	self.ds.addSample(inp, outp)
	# 	print len(self.ds)
	# 	if len(self.ds)==500:
	# 		trainer = BackpropTrainer(self.net, self.ds)
	# 		print 'training'
	# 		trainer.trainUntilConvergence()
	# 		print 'trained'
	# 		i = 0
	# 		for x,y in self.ds:
	# 			if not self.q_old[i] == self.net.activate(x):
	# 				print i, 'old: ', self.q_old[i], 'new: ', self.net.activate(x)
	# 			i+=1
	# 		self.ds.clear()
	# 		self.q_old = np.zeros(500)
