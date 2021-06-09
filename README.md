# DiffusionScripts
Scripts for calculation of diffusion coefficients from LAMMPS MSD output

### msd_mto_each.py

Takes a variable number of independent diffusion calculation as input, each stored in a unique folder with its own MSD file. Preforms multiple time origins (MTO) calculations on each independent run, producing a mto_dat.csv file. The mto_dat.csv files are then averaged across all runs, with the results saved to msd_mto_all.csv. The set of mto_dat.csv files can be used to compute standard deviations for the data. As a default, the script expects MSD data written at a frequency of every 100 time steps, and a time step of 0.5 fs.
