## Install Pymor


As the data to run the exercises lives on Levante, we need to setup the Pymor package on Levante.

The installation is done in 2 steps: 

  1. Clone the repository
  2. Create a virtual environment


### Clone the Pymor repository

```bash
work="/work/$(id -gn)/$USER"
echo "work directory: $work"
cd $work
module load git
git clone https://esm-tools/pymorize.git
cd pymorize
```

### Create a virtual environment
```bash
prefix="$work/pymor_env"
echo "prefix directory: $prefix"

module load python3
conda create --prefix $prefix python=3.10
conda activate $prefix
python -m pip install -e .[fesom]
```

For additional information, check out the following links

- Creating Virtual environments on Levante: [Python environment locations](https://docs.dkrz.de/blog/2021/conda_path.html#python-environment-locations).
- Installing Pymor: [Pymor documentation](https://pymorize.readthedocs.io/en/latest/installation.html).


## Pymor workshop repository

The Pymor workshop repository contains scripts to run the exercises.

```bash
work="/work/$(id -gn)/$USER"
echo "work directory: $work"
cd $work
git clone https://github.com/esm-tools/pymor_workshop.git
cd pymor_workshop
```

## Get the example data

This workshop is designed for ease-of-use if you are working on DKRZ's Levante system. You can access all of the test data here:

```
/work/ab0995/a270243/pymor_workshop/exercises/data
```

If you want to be able to see the files as part of your own repository, you can make a link

```bash
pwd  # You should be in the root of the repository (`/work/$PROJECT/$USER/pymor_workshop`)
ln -sv /work/ab0995/a270243/pymor_workshop/exercises/data ./exercises/data
```

