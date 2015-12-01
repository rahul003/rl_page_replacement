# for i in range(1,800000):
# 	print i
f = open('data/fin_trace','r')
g = open('data/fin_small_trace','w')
i = 0
for line in f:
	g.write(line)
	if i==800000:
		break
	i+=1