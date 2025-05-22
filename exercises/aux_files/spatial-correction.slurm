#!/bin/bash -e
#SBATCH --job-name=pymorize-controller  # <<< This is the main job, it will launch subjobs if you have Dask enabled.
#SBATCH --account=ab0246                # <<< Adapt this to your computing account!
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --time=00:30:00                 # <<< You may need more time, adapt as needed!

cd /work/ab0246/a270077/SciComp/Projects/pymor-workshop/exercises/aux_files
which pymor
time pymor process spatial-correction.yaml 
