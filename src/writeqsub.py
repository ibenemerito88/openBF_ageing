from string import Template
import os
import sys

network = sys.argv[1]
activity = sys.argv[2]
N = int(sys.argv[3])



# Read template
s = Template(open("qsub.template").read())

# Navigate to network directory
srcdir=os.getcwd()
os.chdir("..")
os.chdir("data")
datadir=os.getcwd()
os.chdir(network)
netdir=os.getcwd()
os.chdir(activity)
actdir=os.getcwd()
for j in range(N):
	f=Template(s.safe_substitute(job=activity+str(j)))
	f=Template(f.safe_substitute(yml=network+str(j)+".yml"))
	f=f.safe_substitute(pat=actdir)

	with open(activity+str(j)+'.qsub','w') as qsub:
		qsub.write(f)
os.chdir(srcdir)

# Copy file for running openBF simulations in Julia
os.system('cp '+os.path.join(srcdir,'obf_sim.jl')+' '+actdir)
