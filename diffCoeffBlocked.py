#! /usr/bin/env python
# Groups n runs into j bins of n/j runs each. Computes diffusion coefficents for each bin ( based only on total MSD, not directional data), then calcualtes the average and standard deviation from the bins. 
# To work, each run in num_runs must have a multiple time origins calculated file, such as would be produced by the 'msd_mto_each' script. Could also be used with pure msd data in a similar format as the mto_dat.csv files (worse stats).
# The current parameters are set for batching a set of 20 independent runs into 4 bins of 5 runs eaach. Runs are batched sequentially (i.e. batch 1 = runs 1:5)
# To calculate statistics without batching, set j=len_runs.
import pandas as pd
import numpy as np

num_runs = list(range(1, 21))
len_runs = len(num_runs)
# If exclusion of any run(s) are desired, add them to the skips list
skips = []

# K tracks the bin number 
k = 0
j = 4 # j is the number of bins
spacing = len_runs/j # spacing = the number of runs in each bin

for num in num_runs:
	if num in skips:	
		continue

	df_add = pd.read_csv('./{0}/mto_dat.csv'.format(num))#, delim_whitespace = True, header = None, names = cols)
	
	if num in list(range(1, len_runs+1, spacing)):
		k = k + 1
		df_overall = pd.DataFrame()
                final = num + spacing# batching into groups of size "spacing"
		print(num, final)
		# Concatanates each individual run's values to an overall df
		for val in list(range(num, final)):
			if val in skips:
				continue
			df_add = pd.read_csv('./{0}/mto_dat.csv'.format(val))#, delim_whitespace = True, header = None, names = cols)
			conct = [df_overall, df_add]
			df_overall = pd.concat(conct)

		# Averages mto data in each group and saves each batch in a seperate file
		df_overall['t'] = df_overall['t']
		overall_avgs = df_overall.groupby('t').mean()
		overall_avgs.to_csv('mto_block_{0}avg.csv'.format(k), ignore_index = True)
		print('MTO {0} done'.format(k))

# Diffusion coefficient calculation for each bin
diff_coeffs = []

# calculate each diiffusion coefficient 
for i in range(1, j+1):
	
	df_mtos = pd.read_csv('mto_block_{0}avg.csv'.format(i))
	df_mtos['total'] = df_mtos['x'] + df_mtos['y'] + df_mtos['z']
	msdt_overall = df_mtos['total']/df_mtos['t']
	D_intermed = np.mean(msdt_overall[-2500:])
	D = D_intermed/6
	diff_coeffs.append(D)

mean_diff = np.mean(diff_coeffs)
stdev = np.std(diff_coeffs, ddof = 1) # sample standard deviation

# Unit conversions from angstroms^2/ps to cm^2/s
# Should update conversion to m^2/s
d_avg_cm = (mean_diff * 10 ** 12) / (10 ** 16)
d_stdev_cm = (stdev * 10 ** 12) / (10 ** 16)

# Write out batch coefficients and overall average, standard deviation 
with open('batch_diffusivity_results.txt', 'w') as w:
	w.write('Diffusion coefficients for 10 batches in angstroms squared per ps:\n')
	for dif in diff_coeffs:
		w.write('{0}\n'.format(dif))

	w.write('Average Diffusion Coefficient: {0}\n'.format(mean_diff))
	w.write('In cm^2/s: {0}\n'.format(d_avg_cm))
	w.write('Standard Deviation: {0}\n'.format(stdev))
	w.write('In cm^2/s: {0}'.format(d_stdev_cm))
	
#print(diff_coeffs)
#print(stdev)
#print(mean_diff)	
