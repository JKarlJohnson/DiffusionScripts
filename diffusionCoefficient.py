#! /usr/bin/env python
# Calculates diffusion coefficent in the x,y,z directions and as a total.
import pandas as pd
import numpy as np

# Read overall mto data file in
# Input file is overall multiple time origins file produced by 'msd_mto_each' python script. The mto file produced for each independent run can also be used as input to get directional diffusivities for each run.
msd_file = 'msd_mto_all.csv'
df = pd.read_csv(msd_file)

# Calculate msd/t values for each direction and total
#print(df[-1:])
msdt_x = df['x']/df['t']
msdt_y = df['y']/df['t']
msdt_z = df['z']/df['t']
msdt_tot = (df['x'] + df['y'] + df['z']) / df['t']

# Save values for viewing of msd/t values (not needed)
d_vals =pd.DataFrame({'x': msdt_x, 'y': msdt_y, 'z': msdt_z, 'total': msdt_tot})
#d_vals.to_csv('msd_divideby_t.csv', ignore_index = True)

# calculate diffusion coefficient from the last 2500 steps
d_x = np.mean(msdt_x[-2500:])/2
d_y = np.mean(msdt_y[-2500:])/2
d_z = np.mean(msdt_z[-2500:])/2
d_tot = np.mean(msdt_tot[-2500:])/6

# Unit conversions from angstroms^2/ps to cm^2/s
# Update to m^2/s (better units)
d_x_cm = (d_x * 10 ** 12) / (10 ** 16)
d_y_cm = (d_y * 10 ** 12) / (10 ** 16)
d_z_cm = (d_z * 10 ** 12) / (10 ** 16)
d_tot_cm = (d_tot * 10 ** 12) / (10 ** 16)

# writes out xyz coefficients and total
with open('directional_difussivity.txt', 'w') as w:
	w.write('Diffusion Coefficients\n')
	w.write('In Units of Angstroms^2/ps:\nx: {0}\ny: {1}\nz: {2}\nTotal: {3}'.format(d_x, d_y, d_z, d_tot))
	w.write('\n\n\n In Units of cm^2/s:\nx: {0}\ny: {1}\nz: {2}\nTotal: {3}'.format(d_x_cm, d_y_cm, d_z_cm, d_tot_cm))	

#print(d_x, d_y, d_z, d_tot)
#print(d_x_cm, d_y_cm, d_z_cm, d_tot_cm)
