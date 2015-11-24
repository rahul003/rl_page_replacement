import numpy as np

class State:
	"""
	for each slot in frame, store its pagenumber, inserted time, freq of access, last access time
	functions:
	change to new state, which means may involve just changing any of 4 values for a frame
	"""
	def __init__(self, size, param):
		self.s = np.zeros((size, param))

	def access(self, frame, curr_time):
		self.s[frame][1] += 1
		self.s[frame][2] = curr_time

	def insert(self, frame, page, curr_time):
		# self.s[frame][0] = page
		self.s[frame][0] = curr_time
		self.s[frame][1] = 1
		self.s[frame][2] = curr_time

	def get_vec(self):
		#normalize 
		s_normed = self.s / self.s.max(axis=0)
		return s_normed.flatten()

