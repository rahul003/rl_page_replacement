import cPickle
import math
import random
import numpy as np
from approximator import GradientDescent

class SarsaApprox:
	def __init__(self, state_dim, action_dim, e=0.1, alpha=0.0001, gamma=0.99, lamda=0.9, trained='pickle_fst.pkl'):
		self.actions = list(range(action_dim))
		self.state_dim = state_dim

		self.e = e
		self.alpha = alpha
		self.gamma = gamma
		self.num_feats = state_dim*3 + action_dim
		self.lamda = lamda

		self.eligibility = np.zeros((self.num_feats))
		self.trained = trained
		self.approximator = GradientDescent(self.num_feats, self.alpha)

		# try:
		# 	# pass
		# 	self.approximator = cPickle.load(open(trained))
		# except IOError, e:
		# 	print 'trained file not found'
		# 	# self.approximator = NNet(self.num_feats, 100)

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
				if index==0:
					max_value = cur_value
					max_action = 0
					
				elif cur_value>max_value:
					max_value = cur_value
					max_action = index
			action = max_action
		return action

	def sa_to_input(self, state, action):
		#action is int
		actions_vec = np.zeros(len(self.actions))
		actions_vec[action] = 1		
		#s,a pair
		return np.concatenate([state.get_vec(), actions_vec])

	def qvalue(self, state, action):
		#q value for s,a
		cur_value = self.approximator.getY(self.sa_to_input(state, action))
		return cur_value

	def act(self, state):
		"""
		or use boltzmann exploration: refer solar boat thesis paper
		"""
		action = self.e_greedy(state)
		return action


	def update_q(self, state, action, reward, new_state, new_action):
		q_old = self.qvalue(state, action)
		q_new = self.qvalue(new_state, new_action)
		delta = reward + (self.gamma*q_new)-q_old
		# print q_old, q_new, reward, 0.9*q_new, 0.9*q_new-q_old, delta
		self.eligibility = self.gamma * self.lamda* self.eligibility + self.approximator.gradient(self.sa_to_input(state, action))
		self.approximator.update(delta, self.eligibility)


	def save_model(self):
		fp = open(self.trained, "w")
		cPickle.dump(self.approximator, fp)
		fp.close()
