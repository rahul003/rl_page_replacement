#!/usr/bin/env python
import argparse
import random
import numpy
from numpy import where
from utils import file_len
from abc import ABCMeta, abstractmethod
from state import State
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from agents import NNSarsa
class FrameTable(object):
	__metaclass__ = ABCMeta

	frames = None
	faults = 0
	time = 0
	current_state = None

	def __init__(self, size):
		FrameTable.frames = numpy.zeros(size, dtype=numpy.int)
		FrameTable.current_state = State(size, 4)
		
	def print_faults(self):
		print FrameTable.faults

	@abstractmethod
	def insert_data(self, frame):
		raise NotImplementedError("Must override insert_data")

	@abstractmethod
	def eject(self):
		raise NotImplementedError("Must override eject")

	@abstractmethod
	def hit(self, p):
		raise NotImplementedError("Must override hit")

	def access(self, page):
		#Attempt to access a given page. returns False if fault
		FrameTable.time += 1

		found_page = where(FrameTable.frames==page)[0]
		if found_page.size == 0:
			#page fault
			self.insert(page)
			return False
		else:
			#page found
			self.hit(found_page[0])
			return True

	def insert(self, page):
		#page fault
		FrameTable.faults += 1

		zero_frames = where(FrameTable.frames==0)[0]
		if zero_frames.size:
			#frame with page 0 found
			FrameTable.frames[zero_frames[0]] = page
			FrameTable.current_state.insert(zero_frames[0], page, FrameTable.time)
			self.insert_data(zero_frames[0])

		else:
			#frame to be ejected
			frame = self.eject()
			FrameTable.frames[frame] = page
			FrameTable.current_state.insert(frame, page, FrameTable.time)
			self.insert_data(frame)
			
class Randomly(FrameTable):
	"""randomly ejects pages when there is a page fault."""

	def insert_data(self, frame):
		pass

	def hit(self, frame):
		FrameTable.current_state.access(frame, FrameTable.time)

	def eject(self):
		return random.randint(0, FrameTable.frames.shape[0] - 1)

class FIFO(FrameTable):
	"""ejects pages according to the order in which they were inserted."""

	def __init__(self, size):
		FrameTable.__init__(self,size)
		#for fifo
		self.insert_times = numpy.zeros(size, dtype=numpy.int)

	def hit(self, frame):
		FrameTable.current_state.access(frame, FrameTable.time)

	def insert_data(self, frame):
		self.insert_times[frame] = FrameTable.time

	def eject(self):
		return numpy.argmin(self.insert_times)

class LRU(FrameTable):
	"""ejects pages which have been the least recently used."""

	def __init__(self, size):
		FrameTable.__init__(self,size)
		#for LRU #init value doesnt matter as init value will nto be queired
		self.access_times = numpy.zeros(size, dtype=numpy.int)
	
	def insert_data(self, frame):
		self.access_times[frame] = FrameTable.time

	def hit(self, frame):
		self.access_times[frame] = FrameTable.time 
		FrameTable.current_state.access(frame, FrameTable.time)

	def eject(self):
		ejected_page = numpy.argmin(self.access_times)
		self.access_times[ejected_page] = numpy.iinfo(numpy.int).max
		return ejected_page

class NFU(FrameTable):
	"""ejects pages according to the not frequently used algorithm."""

	def __init__(self, size):
		FrameTable.__init__(self,size)
		#forNFU
		self.access_counts = numpy.zeros(size, dtype=numpy.int)
	
	def insert_data(self, frame):
		self.access_counts[frame] = 1

	def hit(self, frame):
		self.access_counts[frame] +=1
		FrameTable.current_state.access(frame, FrameTable.time)

	def eject(self):
		ejected_page = numpy.argmin(self.access_counts)
		if(self.access_counts[ejected_page]==0):
			print 'Error'
		return ejected_page

class Optimal(FrameTable):
	"""looks into the future in order to implement the optimal page replacement algorithm."""

	def eject(self):
		max_index = 0
		max_frame = FrameTable.frames[0] #this will be used only in case of last trace page. doesnt mattter

		for frame in FrameTable.frames:
			next_occurences = where(self.trace[self.k+1:] == frame)[0]
			if next_occurences.size:
				index = self.k+1+next_occurences[0]
				if index>max_index:
					max_index = index
					max_frame = frame
			else:
				max_frame = frame
				break
		ind = where(FrameTable.frames == max_frame)[0][0]
		return ind
	
	def hit(self, frame):
		pass
	def insert_data(self, frame):
		pass
	
	def simulate(self, trace):
		self.trace = trace
		for k in range(0, trace.shape[0]):            
			self.k = k
			self.access(trace[k])

class Master(FrameTable):
	def __init__(self, size):
		FrameTable.__init__(self, size)
		
		self.algorithms = []
		self.algorithms.append(Randomly(size))
		self.algorithms.append(FIFO(size))
		self.algorithms.append(LRU(size))
		self.algorithms.append(NFU(size))
		self.curalgo = 2

		self.agent = NNSarsa(size, len(self.algorithms))
		#train to make all inputs go to 10/100 (?)
		self.miss_reward = -1
		self.hit_reward = 0

	def access(self, page):
		#Attempt to access a given page
		state = FrameTable.current_state
		action = self.agent.act(state)
		
		if not action == self.curalgo:
			self.curalgo = action

		if not FrameTable.access(self, page):
			#page fault
			reward = self.miss_reward
		else:
			#hit
			reward = self.hit_reward
		
		new_state = FrameTable.current_state
		new_action = self.agent.act(new_state)
		self.agent.update_q(state, action, reward, new_state, new_action)
		
		if not FrameTable.time%1000:
			self.agent.save_nnet()

	def hit(self, p):
		for algo in self.algorithms:
			algo.hit(p)
	
	def insert_data(self, frame):
		for algo in self.algorithms:
			algo.insert_data(frame)	

	def eject(self):
		# self.curalgo = FrameTable.time%4
		return self.algorithms[self.curalgo].eject()


def GetCommandLineArgs():
	parser = argparse.ArgumentParser(description='simulates page replacement algorithms')
	parser.add_argument('frames', type=int, help='number of frames to simulate')
	parser.add_argument('source', help='filepath of pages to be accessed. one on each line.')
	parser.add_argument('algorithm', help='paging algorithm to use. <0: Random> <1: FIFO> <2: LRU> <3: Clock> <4: Optimal> <5: Custom>', default='0')
	args = parser.parse_args()
	return args

def SimulateStandardAlgo():
	algorithms = {
		'0': {'name': 'RANDOM', 'impl': Randomly},
		'1': {'name': 'FIFO', 'impl': FIFO},
		'2': {'name': 'LRU', 'impl': LRU},
		# '3': {'name': 'CLOCK', 'impl': Clock},
		'4': {'name': 'NFU', 'impl': NFU},
		'5': {'name': 'OPTIMAL', 'impl': Optimal},
	}

	random.seed()
	args = GetCommandLineArgs()

	k = args.algorithm
	# for k in args.algorithm.split(','):
	# # for k in ['0','1','2','4','5']:
	if k=='5':
		trace = numpy.zeros(file_len(args.source), dtype=numpy.int)
		count = 0
	else:
		frame_table = algorithms[k]['impl'](args.frames)

	with open(args.source) as f:
		for line in f:
			if line.strip():
				if k!='5':            
					frame_table.access(int(line.strip()))
				else:
					trace[count] = int(line.strip())
					count+=1

	if k=='5':
		frame_table = algorithms[k]['impl'](args.frames)
		frame_table.simulate(trace)

	print algorithms[k]['name']
	frame_table.print_faults()

def SimulateMaster():
	random.seed()
	args = GetCommandLineArgs()

	frame_table = Master(args.frames)
	with open(args.source) as f:
		for line in f:
			if line.strip():
				frame_table.access(int(line.strip()))
				
	print 'Master performance: '
	frame_table.print_faults()

if __name__ == "__main__":
	SimulateMaster()
	# SimulateStandardAlgo()