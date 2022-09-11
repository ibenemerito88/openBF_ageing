# openBF_ageing

[openBF](https://github.com/INSIGNEO/openBF) is an open-source 1D blood flow solver based on MUSCL finite-volume numerical scheme, written in [Julia](https://julialang.or) and developed at [The University of Sheffield](https://www.sheffield.ac.uk). 

This repository contains a set of Python3 scripts for generating openBF configuration files that describe the process of ageing of the cardiovascular system. These scripts have been developed at The University of Sheffield as part of the EU project [CompBioMed2](https://www.compbiomed.eu/). 

## Usage
To use it, run the Python3 command

```
launch.py "<network name>" "<study name>" "<subjects per age>"
```

The script will read the input files inside the directory ```data/"<network name">"``` , which must be created beforehand, sample the input parameter space and create ```"<subjects per age>"``` virtual subjects for each of the desired ages. openBF configuration files and simulation results are saved in ```data/"<study name>"```, which is created during the sampling process. 


## Simple documentation
- **```launch.py```**
This script manages the ageing modelling, preparation of HPC submission files, and reading and saving of input and output files.

- **```sample.py```**
 This script samples the parameters for the aged models and writes the input files for openBF simulations (```.yml``` network files and ```.dat``` inlet files). The following configuration files, read at runtime, defined the baseline parameters of the network: 
  - ```ages.age``` text file containing the ages that are simulated.
  - ```radius.baseline``` baseline values of vessel radii. These are modified with ageing.
  - ```length.baseline``` baseline values of vessel length. This is not modified over time in the current implementation but modification to the code can be easily implemented.
  - ```resistance.baseline``` baseline values of peripheral resistance. These are modified with ageing.
  - ```compliance.baseline``` baseline values of peripheral compliance. These are modified with ageing.
  - ```stiffness.baseline``` baseline values of vessel stiffness. These are modified with ageing.
  - ```inlet.baseline``` baseline values of inlet flow. This is modified with ageing.

The underlying assumption behind modelling of aged cardiovascular networks is that all the parameters are scaled uniformly and according to their own characteristic ageing function (e.g. all radii are scaled by their characteristic parameter, and all stiffness are scaled by their own characteristic parameter). Currently, the implemented hypothesis is that ageing functions are normally distributed. Mean values of the ageing functions are contained in ```ageing.mean``` and ```ageing.std``` as tables. The rows of the tables indicate the variable (radius, stiffness, thickness, peripheral resistance, peripheral compliance, cardiac output), while the column indicate mean or standard deviation at a specific age. 


- **```extractinput.py```**
After the openBF simulations have been run, the script ```extractinput.py``` reads the solutions, checks which one have reached convergence, and saves the input parameters for such simulations.

- **```extractwaveform.py```**
This script reads the configuration file ```data/"<network name">.wave```, which specifies the waveform type (flow rate, pressure, blood velocity, vessel area, wave speed) and the arteries of interest. For each line in the configuration file the script saves a text file named ```"<network name>"_"<activity name>"_"<artery>"_"<type>".wave``` in the directory ```data/"<network name">/"<study name>"```

- **```writeqsub.py```**
This script writes the submission files for launch the openBF simulations on HPC systems with [SGE scheduler](http://star.mit.edu/cluster/docs/0.93.3/guides/sge.html). A template must be provided in the ```src``` directory.


## Provided example
This repository contains the file necessary for modelling the ageing of a simple circulatory model, shown below:

![image](https://github.com/ibenemerito88/images/blob/main/bifurcation.png)

  To generate the openBF files simply navigate to the directory ```src``` and run 

```
python3 launch.py bifurcation A 10
```

This will generated 10 virtual patient for each age in [25, 35, 45, 55, 65, 75] years, and will save their configuration files inside the study directory ```data/bifurcation/A```


