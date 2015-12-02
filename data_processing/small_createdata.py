# f = open('increasing.txt','w')
# for i in range(1,10000000):
# 	f.write(str(i)+'\n')
# f.close()

f = open('alternateNonrepeating.txt','w')
for j in range(0,10):
	for i in range(j,j+600):
		f.write(str(i)+'\n')
f.close()

# f = open('changingpatterns_freq.txt','w')
# g = open('largealternate.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# h = open('fin_trace.txt','r')
# hlines = []
# for line in h:
# 	hlines.append(line)
# gi = 0
# hi = 0
# for i in range(1,1200):
# 	if i%2:
# 		for j in range(gi,gi+500):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 	else:
# 		# print num_equal(hlines[hi:hi+500],glines[gi:gi+500])
# 		for j in range(hi,hi+500):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# f.close()


# f = open('changingpatterns.txt','w')
# g = open('largealternate.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# h = open('fin_trace.txt','r')
# hlines = []
# for line in h:
# 	hlines.append(line)
# gi = 0
# hi = 0
# for i in range(1,500):
# 	if i%2:
# 		for j in range(gi,gi+1200):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 	else:
# 		# print num_equal(hlines[hi:hi+500],glines[gi:gi+500])
# 		for j in range(hi,hi+1200):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# f.close()


# f = open('changingpatterns_lessfreq.txt','w')
# g = open('largealternate.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# h = open('fin_trace.txt','r')
# hlines = []
# for line in h:
# 	hlines.append(line)
# gi = 0
# hi = 0
# for i in range(1,200):
# 	if i%2:
# 		for j in range(gi,gi+3000):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 	else:
# 		# print num_equal(hlines[hi:hi+500],glines[gi:gi+500])
# 		for j in range(hi,hi+3000):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# f.close()


# # # random, then photo gallery
# f = open('changingpatterns_withincreasing.txt','w')
# g = open('increasing.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# h = open('fin_trace.txt','r')
# hlines = []
# for line in h:
# 	hlines.append(line)
# gi = 0
# hi = 0
# for i in range(1,500):
# 	if i%2:
# 		for j in range(gi,gi+1200):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 	else:
# 		for j in range(hi,hi+1200):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# f.close()

# f = open('mix','w')
# g = open('increasing.txt','r')
# h = open('fin_trace.txt','r')
# i = open('largealternate.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# hlines = []
# for line in h:
# 	hlines.append(line)
# ilines = []
# for line in i:
# 	ilines.append(line)
# gi = 0
# hi = 0
# ii = 0
# for k in range(0,800):
# 	if k%3 ==0:
# 		for j in range(gi,gi+1000):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 		gi+=1000
# 	elif k%3 == 1:
# 		for j in range(hi,hi+1000):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# 		hi+=1000
# 	elif k%3 == 2:
# 		for j in range(ii,ii+1000):
# 			if ii==len(ilines):
# 				break
# 			f.write(str(ilines[j]))
# 		ii+=1000



# f = open('mix2','w')
# g = open('increasing.txt','r')
# h = open('largealternate.txt','r')
# glines = []
# for line in g:
# 	glines.append(line)
# hlines = []
# for line in h:
# 	hlines.append(line)
# gi = 0
# hi = 0
# for k in range(0,800):
# 	if k%2 ==0:
# 		for j in range(gi,gi+400):
# 			if gi==len(glines):
# 				break
# 			f.write(str(glines[j]))
# 		gi+=1000
# 	elif k%2 == 1:
# 		for j in range(hi,hi+400):
# 			if hi==len(hlines):
# 				break
# 			f.write(str(hlines[j]))
# 		hi+=1000



# f = open('lrugood','w')
# for i in range(0,1000):
# 	f.write(str(i%10)+'\n')
