#!/bin/bash -e
#SBATCH --job-name=pymorize-controller  # <<< This is the main job, it will launch subjobs if you have Dask enabled.
#SBATCH --account=                      # <<< Adapt this to your computing account!
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --time=00:30:00                 # <<< You may need more time, adapt as needed!

#loadconda
module load python3
source $(conda info --base)/etc/profile.d/conda.sh
conda activate pymor
time pymor process spatial-correction.yaml 
