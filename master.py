from pralgos import FrameTable, Randomly, FIFO, LRU, NFU, Optimal, MRU
from agent import SarsaApprox
import random
import sys
import numpy

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

class Master(FrameTable):
	def __init__(self, size, reward_style='simple'):
		FrameTable.__init__(self, size)
		
		self.algorithms = []
		# self.algorithms.append(Randomly(size))
		self.algorithms.append(LRU(size))
		self.algorithms.append(FIFO(size))
		self.algorithms.append(NFU(size))
		self.algorithms.append(MRU(size))
		self.curalgo = 0

		self.agent = SarsaApprox(size, len(self.algorithms))

		self.reward_style = reward_style
		if not reward_style == 'simple':
			self.framefault = {}
		
		self.miss_reward_step = -1
		self.hit_reward_step = 1

		self.ah_files = []
		self.ah_counts = [0,0,0,0]
		for i in range(0, len(self.algorithms)):
			self.ah_files.append(open('actions_history_'+str(i),'w'))

	def get_miss_reward(self):
		if self.reward_style == 'simple':
			return self.miss_reward_step
		elif self.reward_style == 'num_unique_frames':
			return -1*len(self.framefault)

	def get_hit_reward(self):
		return self.hit_reward_step

	def access(self, page):
		#Attempt to access a given page
		# print 'page', page
		state = FrameTable.current_state
		# print 'getting action for current state'
		action = self.agent.act(state)
		self.ah_counts[action]+=1
		for a in range(0,len(self.algorithms)):
			self.ah_files[a].write(str(self.ah_counts[a])+'\n')

		if not action == self.curalgo:
			self.curalgo = action

		if not FrameTable.access(self, page):
			#page fault
			reward = self.get_miss_reward()
		else:
			#hit
			reward = self.get_hit_reward()
	
		new_state = FrameTable.current_state
		new_action = self.agent.act(new_state)
		self.agent.update_q(state, action, reward, new_state, new_action)

		if not FrameTable.time%100:
			self.agent.save_model()

	def hit(self, p):
		for algo in self.algorithms:
			algo.hit(p)
	
	def insert_data(self, frame):
		for algo in self.algorithms:
			algo.insert_data(frame)	

	def eject(self):
		fid = self.algorithms[self.curalgo].eject()
		if self.reward_style == 'num_unique_frames':
			if fid in self.framefault:
				self.framefault[fid]+=1
			else:
				self.framefault[fid]=1
		return fid

	def print_faults(self):
		FrameTable.print_faults(self)
		print self.ah_counts
		for i in range(0,len(self.algorithms)):
			self.ah_files[i].close()

def SimulateStandardAlgo(num_f, filename, k):
	algorithms = {
		'0': {'name': 'RANDOM', 'impl': Randomly},
		'1': {'name': 'FIFO', 'impl': FIFO},
		'2': {'name': 'LRU', 'impl': LRU},
		'3': {'name': 'MRU', 'impl': MRU},
		'4': {'name': 'NFU', 'impl': NFU},
		'5': {'name': 'OPTIMAL', 'impl': Optimal},
	}

	random.seed()
	if k=='5':
		trace = numpy.zeros(file_len(filename), dtype=numpy.int)
		count = 0
		occurences = {}
	else:
		frame_table = algorithms[k]['impl'](num_f)
		frame_table.reset()

	with open(filename) as f:
		for line in f:
			if line.strip():
				if k!='5':            
					frame_table.access(int(line.strip()))
				else:
					key = int(line.strip())
					trace[count] = key
					if key in occurences:
						occurences[key].append(count)
					else:
						occurences[key] = []
						occurences[key].append(count)
					count+=1

	if k=='5':
		frame_table = algorithms[k]['impl'](num_f)
		frame_table.reset()
		frame_table.simulate(trace, occurences)
	print algorithms[k]['name']
	frame_table.print_faults()

def SimulateMaster(num_frames, data_file, reward_style='simple'):
	random.seed()

	frame_table = Master(num_frames, reward_style)
	frame_table.reset()
	with open(data_file) as f:
		for line in f:
			if line.strip():
				frame_table.access(int(line.strip()))
				
	print 'Master performance: '
	frame_table.print_faults()

if __name__ == "__main__":
	# num_f = 500
	# fil = 'data/increasing.txt'
	# SimulateMaster(num_f, fil)
	if(len(sys.argv)==4):
		SimulateStandardAlgo(int(sys.argv[1]), sys.argv[2], sys.argv[3])
	else:
		SimulateMaster(int(sys.argv[1]), sys.argv[2])

	# 	'0': {'name': 'RANDOM', 'impl': Randomly},
	# 	'1': {'name': 'FIFO', 'impl': FIFO},
	# 	'2': {'name': 'LRU', 'impl': LRU},
	# 	'3': {'name': 'MRU', 'impl': MRU},
	# 	'4': {'name': 'NFU', 'impl': NFU}
	# 	'5': {'name': 'OPTIMAL', 'impl': Optimal}