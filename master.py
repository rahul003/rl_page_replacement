from pralgos import FrameTable, Randomly, FIFO, LRU, NFU
from agent import SarsaApprox
import random

class Master(FrameTable):
	def __init__(self, size):
		FrameTable.__init__(self, size)
		
		self.algorithms = []
		self.algorithms.append(Randomly(size))
		self.algorithms.append(FIFO(size))
		self.algorithms.append(LRU(size))
		self.algorithms.append(NFU(size))
		self.curalgo = 2

		self.agent = SarsaApprox(size, len(self.algorithms))
		#train to make all inputs go to 10/100 (?)
		self.miss_reward = -10
		self.hit_reward = 0

		self.actions_history = {0:0,1:0,2:0,3:0}

	def access(self, page):
		#Attempt to access a given page
		state = FrameTable.current_state
		action = self.agent.act(state)
		self.actions_history[action]+=1
		
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
		return self.algorithms[self.curalgo].eject()

	def print_faults(self):
		FrameTable.print_faults(self)
		print self.actions_history

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

def SimulateMaster(num_frames, data_file):
	random.seed()
	# args = GetCommandLineArgs()

	frame_table = Master(num_frames)
	c=0
	with open(data_file) as f:
		for line in f:
			if line.strip():
				if c>1000:
					break
				frame_table.access(int(line.strip()))
				c+=1
				
	print 'Master performance: '
	frame_table.print_faults()

if __name__ == "__main__":
	SimulateMaster(100, 'data/fin_small_trace')
	# SimulateStandardAlgo()