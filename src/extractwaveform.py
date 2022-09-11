import numpy as np
import os
import sys

def extract_waveform(network,conv,vessel,variable):
	N=len(conv)
	wavef=[]
	for i in conv:
		os.chdir(network+str(i)+"_results")
		wavef.append(np.loadtxt(vessel+"_"+variable+".last")[:,3])
		os.chdir("..")
	wavef=np.array(wavef)
	np.savetxt(network+"_"+activity+"_"+vessel+"_"+variable+".wave",wavef)
	print("Saved: "+network+"_"+activity+"_"+vessel+"_"+variable+".wave")



network = sys.argv[1]
activity = sys.argv[2]

srcdir=os.getcwd()
os.chdir("..")
os.chdir("data")
datadir=os.getcwd()
os.chdir(network)
netdir=os.getcwd()
varvessel=open(network+".wave").read().splitlines()
os.chdir(activity)

# check convergence
conv=np.loadtxt(network+'_'+activity+".conv").astype(int)
for v in varvessel:
	extract_waveform(network,conv,v.split('_')[0],v.split('_')[1])




os.chdir(srcdir)














