#!/bin/python3

import os
import time
import sys
import numpy as np



def continuerunning():
	os.system('qstat > jobs.txt')
	go = 0
	joblist = open("jobs.txt").read().splitlines()
	total_jobs = len(joblist)-2
	how_many_bash = 0
	for i in range(2,len(joblist)):
	        if 'bash' in joblist[i]:
	                how_many_bash+=1
	how_many_submitted = len(joblist)-2-how_many_bash
	how_many_qw = 0
	for i in range(2+how_many_bash,len(joblist)):
	        if ' qw ' in joblist[i]:
	                how_many_qw+=1
	how_many_running = 0
	for i in range(2+how_many_bash,len(joblist)):
		if ' r ' in joblist[i]:
			how_many_running+=1
	how_many_t = 0
	for i in range(2+how_many_bash,len(joblist)):
		if ' t ' in joblist[i]:
			how_many_t+=1
	if how_many_qw + how_many_t ==0 + how_many_running == 0:
		go = 1
	return go

network = sys.argv[1]
activity = sys.argv[2]
N = sys.argv[3]		# number of subjects per age
totsim = str(int(N)*6)
srcdir=os.getcwd()
### Create openBF config file
print('### Create openBF config file ###')
os.system("python3 sample.py "+network+" "+activity+" "+N)


"""

openBF simulations are run here.
They can be run either locally or on a HPC machine.
A template for submission script that run on ShARC, the HPC computer of The University of Sheffield, is provided.

To run simulations on HPC systems remove comments from the block below.

"""


### Write qsub file
#print('### Write qsub file ###')
os.system("python3 writeqsub.py "+network+" "+activity+" "+totsim)

"""
### Submit jobs

print('### Submit jobs ###')
os.chdir("../data/"+network+"/"+activity)
for i in range(int(totsim)):
	os.system("qsub "+activity+str(i)+".qsub")
	if np.mod(i+1,750)==0:
		print("Sleeping...")
		time.sleep(301)

# Check when jobs are finished
go = 0
while go==0:
	time.sleep(30)
	print('### Checking jobs... ###')
	go = continuerunning()
"""

os.chdir(srcdir)

"""
# Uncomment block to extract input and waveforms

print('### Extract input ###')
os.system("python3 extractinput.py "+network+" "+activity)
print('### Extract waveform ###')
os.system("python3 extractwaveform.py "+network+" "+activity)

"""