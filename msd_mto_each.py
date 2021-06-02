#! /usr/bin/env python
# Updated to calculate MTO data from MSD for each run, then average into an overall MTO file
# Uses LAMMPS MSD files as input, from any number of independent runs as specified by the user
# Not super fast but it gets the job done
import math as m
import os
import pandas as pd

#variables
thermoFrequency = 100 # print out frequency of MSD data
timeStep = 0.5 #fs

skip_runs = [] # add any sub-folders that should be ignored
# list of independent runs to multiple time orgin. Here folders named 1 through 10 are used. T
# To ignore a folder in the selected range, add it to skip_runs
# Sub-folders containing each independent calculation can also be selected by a list of folder names
num_runs_to_avg = list(range(1, 11)) #["NAMEOFFOLDER1", 'NAMEOFFOLDER2", ...]

for num in num_runs_to_avg:
	if num in skip_runs:
		continue
	infile = open('./{0}/MSDCorrected'.format(num),'r') # read msd file
	trash = infile.readline() #header lines do not contain data we need
	trash = infile.readline()
	trash = infile.readline()
	lines = infile.readlines() #read all data lines
	infile.close()
	yt = []
	yx = []
	yy = []
	yz = []
	j = 0
	for line in lines: #lines are timestep and number of values, x, y, z, total, so we only want every fifth line
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
        		j = j + 1
    		elif j == 4:
        		yt.append(float(line.split()[1]))
        		j = 0
	preX = range(0,len(yt))
	x = [i*thermoFrequency*timeStep for i in preX] #multiply by thermo print frequency and timestep to create l#ist of simulation time

	# Identify the total number of points and store in variable Npts
	Npts = len(yt)
#	print(Npts)
	# We need the number of points divided by 2:
	NptsBy2 = int(Npts/2)
#	print(NptsBy2)
	# Specify the number of points to skip (time between time origins) Adjust this as necessary
	Skip = 1000
	# Compute the number of time origins
	Nto = int(NptsBy2/Skip)
#	print(num)

	rx = []
	ry = []
	rz = []
	for i in range(0,NptsBy2):
		rx.append(yx[i])
		ry.append(yy[i])
    		rz.append(yz[i])

		for j in range(0,Nto):
			rx[i] = rx[i]+yx[i+(j+1)*Skip]-yx[(j+1)*Skip]
			ry[i] = ry[i]+yy[i+(j+1)*Skip]-yy[(j+1)*Skip]
			rz[i] = rz[i]+yz[i+(j+1)*Skip]-yz[(j+1)*Skip]

		rx[i]/=(Nto+1)
		ry[i]/=(Nto+1)
		rz[i]/=(Nto+1)

	# Conversion to picoseconds
	t = []
	for i in range(len(rx)):
		t.append(x[i]/1000)

	# totsl msd calcualtion
	total = [x + y + z for x,y,z in zip(rx, ry, rz)]

	# writing individual run's MTO data
	# These can be deleted if only the overall averaged data is desired
	df_mtos = pd.DataFrame({'t': t, 'x': rx, 'y': ry, 'z': rz, 'total': total})
	df_mtos.to_csv('./{0}/mto_dat.csv'.format(num), index = False)
	print('RUN ', num)

df_overall = pd.DataFrame()

# Concatanates indivdual runs values to an overall df
for num in num_runs_to_avg:
	if len(num_runs_to_avg) == 1:
		print("Only 1 independent run, nothing to average")
		continue
	if num in skip_runs:
		continue
	for root, dirs, files in os.walk('{0}'.format(num)):
		new_df = pd.read_csv(os.path.join(root, 'mto_dat.csv'))
		conct = [df_overall, new_df]
		df_overall = pd.concat(conct)

# Averages each of MSDX, MSDY, MSDZ, MSD_total across all runs, storing it in a final csv file
if len(num_runs_to_avg) > 1:
	overall_avgs = df_overall.groupby('t').mean()
	print('MSD MTO OVERALL DONE')
# Writes the averages to a csv file in the starting (one before each individual run directory) directory
	overall_avgs.to_csv('msd_mto_all.csv')