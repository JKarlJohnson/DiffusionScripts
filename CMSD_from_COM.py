#! /usr/bin/env python
# Calculates corrected MSD from the COM data for the adsorbate molecules. Output is the MSD equivelent for corrected diffusivity.
# Currently compatible with python 2.7.5. 
import math as m
import os
import pandas as pd

# list of independent runs to multiple time orgin
num_runs = ['.']# list(range(4, 6)) #["NAMEOFFOLDER1, 'NAMEOFFOLDER2", ...
skip_runs = []
mass_dict = {3: 39.948} # atom type: mass for all atoms in the guest molecule
mol_mass = sum(mass_dict.values())
sim_length=1000000 # length of each independent production run
COM_freq = 100 # frequency of COM data writing
num_mols = 100 # number of guest molecules in the system

# loop over each simulation
for num in num_runs:
	if num in skip_runs:
		continue
	infile = open('./{0}/COM'.format(num),'r')
	trash = infile.readline() #header alines do not contain data we need
	trash = infile.readline()
	trash = infile.readline()
	lines = infile.readlines() #read all data lines
	infile.close()
	yt = []
	yx = []
	yy = []
	yz = []
	j = 0
	for line in lines: #lines are timestep: number of values, xCOM, yCOM, zCOM
   		if j == 0:
        		j = j+1
    		elif j == 1:
        		yx.append(float(line.split()[1]))
        		j = j + 1
    		elif j == 2:
        		yy.append(float(line.split()[1]))
        		j = j + 1
    		elif j == 3:
        		yz.append(float(line.split()[1]))
        		j = 0

	xMSD = [0]
	yMSD = [0]
	zMSD = [0]
	tMSD = []
	# Calculating correcte "msd" from COM data
	for i in range(1, sim_length/COM_freq+1):
		xMSD = xMSD + [(((yx[i]-yx[0])*num_mols)**2)/(num_mols)]
		yMSD = yMSD + [(((yy[i]-yy[0])*num_mols)**2)/(num_mols)]
		zMSD = zMSD + [(((yz[i]-yz[0])*num_mols)**2)/(num_mols)]
	
	# Total "msd" calculation
	tMSD = [x+y+z for x, y, z in zip(xMSD, yMSD, zMSD)]
	t = list(range(0, sim_length/COM_freq+1))
	times = [k*COM_freq for k in t] # timesteps

	# Write MSDC out in style legivle by multiple time origin code
	with open("./{0}/MSDC_COM123".format(num), 'w') as w:

		w.write(" ### Corrected MSD Calculated from Adsorbate Center of Mass\n ###\n ###\n")

		for i in t:
			w.write("{0} 4\n".format(times[i]))
			w.write("1 {0}\n".format(xMSD[i]))
			w.write("2 {0}\n".format(yMSD[i]))
			w.write("3 {0}\n".format(zMSD[i]))
			w.write("4 {0}\n".format(tMSD[i]))

	
