import numpy as np 
# a = np.ones((100*3))
#a a a a a....b b b b b b b.b....c c c c.....

# def boom():	
# 	a[1*100+1]+=1
# 	a[1*100+1]=0.5
# 	s = 0
# 	t = 0
# 	q = 0
# 	for i in range(0,100):
# 		s+=a[i]
# 		t+=a[1*100+i]
# 		q+=a[2*100+i]
# 	for i in range(0,100):
# 		a[i]/=s
# 		a[1*100+i]/=t
# 		a[2*100+i]/=q
# 	return a
a = np.ones((100,3))

def boom():	
	a[1][0]+=1
	a[1][0]=0.5
	return (a/a.max(axis=0)).flatten()

for i in range(0, 10000000):
	c = boom()