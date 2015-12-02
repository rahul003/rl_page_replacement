
class TraceData:
	def __init__(self, filepath):
		self.filepath = filepath
		f = open(filepath,'r')
		self.raw_= []
		for line in f:
			self.raw_.append(line.strip('\n'))
		f.close()
		
		self.trace = []
		self.mapping = {}
		# load_trace()


	def load_trace(self):
		count = 1
		for line in self.raw_:
			if line:
				block = int(line.split(',')[1])
				if block in self.mapping:
					toadd = self.mapping[block]
				else:
					toadd = count
					count+=1
					self.mapping[block] = toadd
				self.trace.append(toadd)
		print len(self.trace)

	def save_trace(self, count):
		g = open(self.filepath+'trace', 'w')
		c = 0
		for k in self.trace:
			if c==count:
				break
			g.write(str(k)+'\n')
			c+=1
		g.close()




if __name__ == "__main__":
	d = TraceData('data/Financial1.spc')
	d.load_trace()
	d.save_trace(10000)

	# g = open('data/Financial1.spctrace','r')
	# c = 0
	# for line in g:
	# 	c+=1
	# 	print line
	# 	if c>100:
	# 		break
