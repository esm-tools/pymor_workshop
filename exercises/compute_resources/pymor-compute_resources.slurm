#!/bin/bash -e
#SBATCH --job-name=pymorize-controller  # <<< This is the main job, it will launch subjobs if you have Dask enabled.
#SBATCH --account=ab0246                # <<< Adapt this to your computing account!
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --time=00:30:00                 # <<< You may need more time, adapt as needed!

module load python3
eval "$(conda shell.bash hook)"
conda activate pymor
which pymor
time pymor process basic.yaml 
