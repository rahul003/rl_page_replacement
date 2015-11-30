#!/usr/bin/env python
import argparse
import random
import numpy
from numpy import where
from utils import file_len
from abc import ABCMeta, abstractmethod
from state import State


class FrameTable(object):
	__metaclass__ = ABCMeta

	frames = None
	faults = 0
	time = 0
	current_state = None

	def __init__(self, size):
		FrameTable.frames = numpy.zeros(size, dtype=numpy.int)
		FrameTable.current_state = State(size, 3)
		self.size = size
	def print_faults(self):
		print FrameTable.faults

	def reset(self):
		FrameTable.frames = numpy.zeros(self.size, dtype=numpy.int)
		FrameTable.faults = 0
		FrameTable.time = 0
		FrameTable.current_state = State(self.size, 3)

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
		return 0
		# return random.randint(0, FrameTable.frames.shape[0] - 1)

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

class MRU(FrameTable):
	"""ejects pages which have been the most recently used."""

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
		ejected_page = numpy.argmax(self.access_times)
		self.access_times[ejected_page] = numpy.iinfo(numpy.int).min
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

