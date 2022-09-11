import numpy as np
import matplotlib.pyplot as plt

from string import Template
import os
import sys
import shutil

"""
radii do not change with age
length does not change with age
thickness does not change with age

stiffness increases with age ONLY in aorta
resistance increase with age
compliance decreases with age

inlet waveform changes with age (but zero standard deviation)

"""

network = sys.argv[1]
activity = sys.argv[2]
N = int(sys.argv[3])	# number of subjects per age

srcdir = os.getcwd()
os.chdir("..")
os.chdir("data")
os.chdir(network)
netdir=os.getcwd()

def create_inlet_file(inlet_baseline,cardiacaged,dat):
	np.savetxt('CoW'+str(dat)+'.dat',np.column_stack([inlet_baseline[:,0],inlet_baseline[:,1]*cardiacaged]))

def baseline_thickness(R):
        # compute baseline thickness from baseline radii
        ah = 0.2802
        bh = 5.053*100
        ch = 0.1324
        dh = 0.1114*100
        return R*(ah*np.exp(-bh*R)+ch*np.exp(-dh*R))

# LOAD INPUT FILES
vnames = open("vessels.name").read().splitlines()	# name of vessels in the network
age = np.loadtxt('ages.age')				# simulated ages

# baseline values
r_baseline = np.loadtxt("radius.baseline")
L_baseline = np.loadtxt("length.baseline")
R1_baseline = np.loadtxt("resistance.baseline")
Cc_baseline = np.loadtxt("compliance.baseline")
E_baseline = np.loadtxt("stiffness.baseline")
inlet_baseline = np.loadtxt("inlet.baseline")
# Compute baseline thickness
h_baseline = baseline_thickness(r_baseline)

# Ageing values: mean and std 
#(radius, stiffness, thickness, peripheral resistance, peripheral compliance, cardiac output)
ageing_mean = np.loadtxt("ageing.mean")	
ageing_std = np.loadtxt("ageing.std")

radius_mean = ageing_mean[0,:]
radius_std = ageing_std[0,:]
stiffness_mean = ageing_mean[1,:]
stiffness_std = ageing_std[1,:]
thickness_mean = ageing_mean[2,:]
thickness_std = ageing_std[2,:]
resistance_mean = ageing_mean[3,:]
resistance_std = ageing_std[3,:]
compliance_mean = ageing_mean[4,:]
compliance_std = ageing_std[4,:]
cardiac_mean = ageing_mean[5,:]
cardiac_std = ageing_std[5,:]

# Arrange ageing values in two dictionaries
r_distr={}
r_distr['mean']={}
r_distr['std']={}
#
E_distr={}
E_distr['mean']={}
E_distr['std']={}
#
h_distr={}
h_distr['mean']={}
h_distr['std']={}
#
R1_distr={}
R1_distr['mean']={}
R1_distr['std']={}
#
Cc_distr={}
Cc_distr['mean']={}
Cc_distr['std']={}
#
cardiac_distr={}
cardiac_distr['mean']={}
cardiac_distr['std']={}
for i in range(len(age)):
	r_distr['mean'][str(age[i])]=radius_mean[i]
	r_distr['std'][str(age[i])]=radius_std[i]
	E_distr['mean'][str(age[i])]=stiffness_mean[i]
	E_distr['std'][str(age[i])]=stiffness_std[i]
	h_distr['mean'][str(age[i])]=thickness_mean[i]
	h_distr['std'][str(age[i])]=thickness_std[i]
	R1_distr['mean'][str(age[i])]=resistance_mean[i]
	R1_distr['std'][str(age[i])]=resistance_std[i]
	Cc_distr['mean'][str(age[i])]=compliance_mean[i]
	Cc_distr['std'][str(age[i])]=compliance_std[i]
	cardiac_distr['mean'][str(age[i])]=cardiac_mean[i]
	cardiac_distr['std'][str(age[i])]=cardiac_std[i]

 
# GENERATE INPUT FILES

names = []	# names of the variables to be substituted in the template
for i in range(len(L_baseline)):
	names.append('l'+str(i+1))
for i in range(len(r_baseline)):
	names.append('r'+str(i+1))
for i in range(len(h_baseline)):
	names.append('h'+str(i+1))
for i in range(len(E_baseline)):
	names.append('e'+str(i+1))
for i in range(len(R1_baseline)):
	names.append('Rt'+str(i+1))
for i in range(len(Cc_baseline)):
	names.append('Cc'+str(i+1))


# import template
s = Template(open(network+".template").read())

totalsubjects = len(age)*N
created = 0	# counter for simulation
dat = 0		# counter for inlet 
ages = []	# all the simulated ages
VALUES = []	# all the input values


### CREATE ACTIVITY FOLDER 
if os.path.isdir(activity):
	shutil.rmtree(activity)
os.mkdir(activity)


for a in age:
	# SAMPLE FROM DISTRIBUTION
	for j in range(N):	# N is the number of subjects per age
		# Agedvalue = multipliers*Baseline
		Laged = L_baseline 	# length is not affected by ageing
		Raged = np.random.normal(r_distr['mean'][str(a)],r_distr['std'][str(a)])*r_baseline
		Eaged = np.random.normal(E_distr['mean'][str(a)],E_distr['std'][str(a)])*E_baseline
		haged = np.random.normal(h_distr['mean'][str(a)],h_distr['std'][str(a)])*h_baseline
		R1aged = np.random.normal(R1_distr['mean'][str(a)],R1_distr['std'][str(a)])*R1_baseline
		Ccaged = np.random.normal(Cc_distr['mean'][str(a)],Cc_distr['std'][str(a)])*Cc_baseline
		# Scaling factor for cardiac output
		cardiacaged = np.random.normal(cardiac_distr['mean'][str(a)],cardiac_distr['std'][str(a)])

		os.chdir(activity)

		# write yml file
		f = Template(s.safe_substitute(created=created))	# simulation number
		f = Template(f.safe_substitute(dat=str(dat)+'.dat'))	# inlet file
		values = np.hstack([Laged,Raged,haged,Eaged,R1aged,Ccaged,cardiacaged])
		VALUES.append(values)
		
		with open(network+str(created)+".yml",'w') as yml:
			yml.write(f.substitute({names[i]:values[i] for i in range(len(names))}))
		# write inlet file
		create_inlet_file(inlet_baseline,cardiacaged,dat)
		created+=1
		dat+=1
		ages.append(a)
		os.chdir("..")

### MOVE INLET DAT FILE TO ACTIVITY DIRECTORY
os.chdir(activity)
activitydir = os.getcwd()
# Save config files
os.system('cp ../*.baseline .')
# Save ages
np.savetxt(network+'_'+activity+'.age',ages)
ages = np.array(ages)
# Save input parameters
VALUES = np.array(VALUES)
np.savetxt(network+'_'+activity+'.values',VALUES)
# Save input variables names
with open(network+'_'+activity+'.names','w') as f:
	for i in names:
		f.write(i+'\n')
f.close()

# copy sample.py
os.system('cp '+srcdir+'/sample.py '+activitydir)

os.chdir(srcdir)
