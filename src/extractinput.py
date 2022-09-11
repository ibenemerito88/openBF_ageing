import numpy as np
import os
import sys

network = sys.argv[1]
activity = sys.argv[2]

srcdir=os.getcwd()
os.chdir("..")
os.chdir("data")
datadir=os.getcwd()
os.chdir(network)
netdir=os.getcwd()
os.chdir(activity)
print(os.getcwd())
# check convergence
conv=[]
a=os.listdir()
for i in a:
	if os.path.isdir(i):
		os.chdir(i)
		if os.path.isfile(i.split('_')[0]+'.conv'):
			conv.append(int(i.split('_')[0].split(network)[1]))
		os.chdir('..')
conv = np.array(conv).astype(int)
conv = np.sort(conv)
np.savetxt(network+'_'+activity+".conv",conv)
os.chdir(srcdir)














