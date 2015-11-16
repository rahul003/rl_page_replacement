#!/usr/bin/env python
import argparse
import random
import numpy
from numpy import where
from utils import file_len


"""
Todo:
move data for an algo into its own class
"""

class Master(object):

	def __init__(self, size):
		"""Create a frame table"""
		self.frames = numpy.zeros(size, dtype=numpy.int)
		self.faults = 0

		self.algorithms = []
		self.algorithms.append(Rand(size))
		self.algorithms.append(FIFO(size))
		self.algorithms.append(LRU(size))
		self.algorithms.append(NFU(size))

		self.curalgo = 0
		self.current_state = State(size)
		
		#fifo, lru
		self.time = 0

		#for fifo
		self.insert_times = numpy.zeros(size, dtype=numpy.int)

		#for LRU #init value doesnt matter as init value will nto be queired
		self.access_times = numpy.zeros(size, dtype=numpy.int)
		
		#forNFU
		self.access_counts = numpy.zeros(size, dtype=numpy.int)


	def access(self, page):
		"""Attempt to access a given page."""
		#fifo, lru
		self.time += 1

		found_page = where(self.frames==page)[0]
		if found_page.size == 0:
			#page fault
			self.insert(page)
		else:
			#page found
			self.access_times[found_page[0]] = self.time 
			self.access_counts[found_page[0]] +=1
			self.state.access(found_page[0], self.time)

	def insert_data(self, frame):
		self.insert_times[frame] = self.time
		self.access_times[frame] = self.time
		self.access_counts[frame] = 1

	def insert(self, page):
		#page fault
		self.faults += 1
		
		zero_frames = where(self.frames==0)[0]
		if zero_frames.size:
			#frame with page 0 found
			self.frames[zero_frames[0]] = page
			self.insert_data(zero_frames[0])
			self.state.insert(zero_frames[0], page, self.time)
		else:
			#frame to be ejected
			frame = self.eject()
			self.frames[frame] = page
			self.insert_data(frame)
			self.state.insert(frame, page, self.time)

	def eject(self):
		#Eject a frame from the frame table according to an algorithm
		#call agent and get action for curstate and set it to curalgo
		return self.algorithms[self.curalgo].eject()

	def print_faults(self):
		"""Print the access table."""
		print self.faults


class Rand(Master):
	"""randomly ejects pages when there is a page fault."""

	def eject(self):
		return random.randint(0, self.frames.shape[0] - 1)

class FIFO(Master):
	"""ejects pages according to the order in which they were inserted."""

	def eject(self):
		return numpy.argmin(self.insert_times)

class LRU(Master):
	"""ejects pages which have been the least recently used."""
	def eject(self):
		ejected_page = numpy.argmin(self.access_times)
		self.access_times[ejected_page] = numpy.iinfo(numpy.int).max
		return ejected_page

class NFU(Master):
	"""ejects pages according to the not frequently used algorithm."""

	def eject(self):
		ejected_page = numpy.argmin(self.access_counts)
		if(self.access_counts[ejected_page]==0):
			print 'Error'
		return ejected_page

class Optimal(Master):
	"""looks into the future in order to implement the optimal page replacement algorithm."""

	def eject(self):
		max_index = 0
		max_frame = self.frames[0] #this will be used only in case of last trace page. doesnt mattter

		for frame in self.frames:
			next_occurences = where(self.trace[self.k+1:] == frame)[0]
			if next_occurences.size:
				index = self.k+1+next_occurences[0]
				if index>max_index:
					max_index = index
					max_frame = frame
			else:
				max_frame = frame
				break
		 ind = where(self.frames == max_frame)[0][0]
		return ind

	def simulate(self, trace):
		self.trace = trace
		for k in range(0, trace.shape[0]):            
			self.k = k
			self.access(trace[k])


def GetCommandLineArgs():
	parser = argparse.ArgumentParser(description='Simulates a number of different virtual memory page replacement algorithms.')
	parser.add_argument('frames', type=int, help='The number of frames to simulate.')
	# parser.add_argument('algorithm', help='The paging algorithm to use. <0: Random> <1: FIFO> <2: LRU> <3: Clock> <4: Optimal> <5: Custom>')
	parser.add_argument('source', help='File containing a string of integers representing pages to be accessed.')
	args = parser.parse_args()

def SimulateStandardAlgos():
	algorithms = {
		'0': {'name': 'RANDOM', 'impl': Rand},
		'1': {'name': 'FIFO', 'impl': FIFO},
		'2': {'name': 'LRU', 'impl': LRU},
		# '3': {'name': 'CLOCK', 'impl': Clock},
		'4': {'name': 'NFU', 'impl': NFU},
		'5': {'name': 'OPTIMAL', 'impl': Optimal},
	}

	random.seed()
	args = GetCommandLineArgs()

	for k in ['0','1','2','4','5']:
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

	
	frame_table = algorithms[k]['impl'](args.frames)
	with open(args.source) as f:
		for line in f:
			if line.strip():
				frame_table.access(int(line.strip()))
				
	print 'Master performance: '
	frame_table.print_faults()


if __name__ == "__main__":
	SimulateMaster()