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

def increasing():
	f = open('increasing.txt','w')
	for i in range(1,10000000):
		f.write(str(i)+'\n')
	f.close()

def large_alternate(num=1000):
	f = open('largealternate.txt','w')
	for j in range(0,num):
		for i in range(1,600):
			f.write(str(i)+'\n')
	f.close()

def mix():
	#changing access patterns	
	f = open('mix','w')
	g = open('increasing.txt','r')
	h = open('fin_trace.txt','r')
	i = open('largealternate.txt','r')
	glines = []
	for line in g:
		glines.append(line)
	hlines = []
	for line in h:
		hlines.append(line)
	ilines = []
	for line in i:
		ilines.append(line)
	gi = 0
	hi = 0
	ii = 0
	for k in range(0,800):
		if k%3 ==0:
			for j in range(gi,gi+1000):
				if gi==len(glines):
					break
				f.write(str(glines[j]))
			gi+=1000
		elif k%3 == 1:
			for j in range(hi,hi+1000):
				if hi==len(hlines):
					break
				f.write(str(hlines[j]))
			hi+=1000
		elif k%3 == 2:
			for j in range(ii,ii+1000):
				if ii==len(ilines):
					break
				f.write(str(ilines[j]))
			ii+=1000


def mix2():
	f = open('mix2','w')
	g = open('increasing.txt','r')
	h = open('largealternate.txt','r')
	glines = []
	for line in g:
		glines.append(line)
	hlines = []
	for line in h:
		hlines.append(line)
	gi = 0
	hi = 0
	for k in range(0,800):
		if k%2 ==0:
			for j in range(gi,gi+400):
				if gi==len(glines):
					break
				f.write(str(glines[j]))
			gi+=1000
		elif k%2 == 1:
			for j in range(hi,hi+400):
				if hi==len(hlines):
					break
				f.write(str(hlines[j]))
			hi+=1000

			
if __name__ == "__main__":
	# d = TraceData('data/Financial1.spc')
	# d.load_trace()
	# d.save_trace(10000)

	# mix()