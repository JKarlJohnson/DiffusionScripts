#!/usr/bin/env bash

#SBATCH --job-name=UIO-66Ar20.run.298
#SBATCH --cluster=mpi
#SBATCH --partition=ib
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jjw101@pitt.edu
#SBATCH --time=3-00:00:00


module purge
module load intel/2018.2.199  intel-mpi/2018.2.199
module load lammps/16Mar18

INP=in.MFI.Ar

mpirun -np $SLURM_NTASKS lmp_mpi -sf opt -in $INP

crc-job-stats.py # gives stats of job, wall time, etc.

