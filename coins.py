vals = [2, 5, 3, 9, 7]
used = [0, 0, 0, 0, 0]

for i1 in xrange(0, 5):
	used[i1] = 1
	for i2 in xrange(0, 5):
		if used[i2] == 1:
			continue
		used[i2] = 1
		for i3 in xrange(0, 5):
			if used[i3] == 1:
				continue
			used[i3] = 1
			for i4 in xrange(0, 5):
				if used[i4] == 1:
					continue
				used[i4] = 1
				for i5 in xrange(0, 5):
					if used[i5] == 1:
						continue
					if vals[i1]+vals[i2]*vals[i3]**2+vals[i4]**3-vals[i5] == 399:
						print (vals[i1], vals[i2], vals[i3], vals[i4], vals[i5])
				used[i4] = 0
			used[i3] = 0
		used[i2] = 0
	used[i1] = 0


