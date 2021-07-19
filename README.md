# DiffusionScripts
Scripts for calculation of diffusion coefficients from LAMMPS MSD output

### msd_mto_each.py

Takes a variable number of independent diffusion calculation as input, each stored in a unique folder with its own MSD file. Preforms multiple time origins (MTO) calculations on each independent run, producing a mto_dat.csv file. The mto_dat.csv files are then averaged across all runs, with the results saved to msd_mto_all.csv. The set of mto_dat.csv files can be used to compute standard deviations for the data. As a default, the script expects MSD data written at a frequency of every 100 time steps, and a time step of 0.5 fs.


### diffusionCoefficient.py

Calculates self-diffusion coefficients in each direction (D_x, D_y, D_z) as well as the overall diffusion coefficient from a single file in the format outputted by msd_mto_each.py. Can be used with the overall file (msd_mto_all.csv), or the intermediate files produced within each independent run's folder (mto_dat.csv). Run script from the same folder as the msd file to read from. Writes out diffusion coefficients to file: directionalDiffusivity.txt in format:

Diffusion Coefficients\n
In units Angstroms^2/ps:\n
x: Ds_x\n
y: Ds_y\n
z: Ds_z\n
Total: Ds_tot\n\n

In units of cm^2/s:
x: Ds_x_converted
y: Ds_y_converted
z: Ds_z_converted
Total: Ds_tot_converted

### diffCoeffBlocked.py

Calcualtes average and standard deviation of diffusion coefficients across independent calculations. Can batch runs before averaging (for example, given 20 independent runs 5 batches of 4 simulations could be preformed) or it can treat each simulation independently. The latter will likely result in greater standard deviations, but is less ambiguous than the batching method. This script only looks at the total diffusion coefficients, but could be fairly easily updated to preform calculations for each directional diffusivity as well. Run script from parent directory containing each independent simulation folder, just as you would when running msd_mto_each.py. Writes diffusion coefficients out to file batch_diffusivity_results.txt in the following format:

Header line
Ds batch 1
Ds batch 2
. . .
Ds batch n
Average diffusion coefficient: Ds_avg
In cm^2/s: Ds_avg_converted
Standard Deviation: std(Ds_avg)
In cm^2/s: std(Ds_avg_converted)
