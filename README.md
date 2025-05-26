# Pymor Workshop

Clone this repository to get access to the slides and practice problems:

```
$ git clone https://github.com/esm-tools/pymor_workshop.git
$ cd pymor_workshop
$ mkdir work
```

Make a folder to work in, for example:
```
$ cd work
```

---

## Outline

### 1. Intro
  * Workshop intro @pgierz 
    * Aims
    * Outline
  * Pymor @siligam 
    * What is Pymor?
    * Main Pymor features
  * Demo: check that pymor works and show cli (`pymor --help`, `pymor compute --help` ...) @pgierz
  * Time to resolve installation problems @pgierz
    * Have you installed Pymor inside a conda environment named `pymor` already?
    * Can you run `pymor --help` and other commands?
### 2. Basic yaml syntax
  * Description of the most basic features of pymor @pgierz 
  * Exercise: basic (first part only one variable, second part 2 variables with common parameters controlled in the `inherit` key) @pgierz 
### 3. Features
#### 3.1. Units (`module_units` and `cmor_units`)
* Presentation
* Exercise: wrong units in source data 
#### 3.2. Dimensionless units mapping
* Presentation
* Exercise: how to contribute to dimensionless mappings yaml
#### 3.3. Time span for output files (`file_timespan`)
* Presentation
* Exercise: going from 12 files (one per month) to 1 file (12 timesteps in one complete file)
#### 3.4. Time averages
* Presentation
* Exercise: exercise where input is in daily and table request the frequency in months
#### 3.5. Adjusting time stamps of steps
* [Presentation]()
* Exercise: [Adjust timestamp](https://github.com/esm-tools/pymor_workshop/blob/main/exercises/adjust_timestamp.md)
#### 3.6. Control computing resources
* Presentation (which features are available to control computing resources? Dask vs Prefect)
* Exercise: change number of nodes used
#### 3.7. Pipelines and custom steps
* Presentation
* Exercise: add a custom step
#### 3.8. Combining model output variables
* Presentation
* Exercise: Custom step to add multiple variables into one
#### 3.9. PyFESOM
* Presentation (pyfesom and external packages)
* Exercise: custom step using pyfesom features?
### 4. Try Pymor with your data
### 5. Close the workshop

---

## Install Pymor

As the data to run the exercises lives on Levante,(DKRZ), we need to setup the Pymor package on Levante.

The installation is done in 2 steps:

  1. Create a virtual environment
  2. Install Pymor

### Create a virtual environment

**Note:** the exercises assume you have a `pymor` conda environment, so make sure when you create the environment that its name matches that.

```bash
module load python3
eval "$(conda shell.bash hook)"      # Init conda without the need to add extra lines to ~/.bashrc
conda create -n pymor python=3.10    # Create a conda environment named pymor
```

### Install Pymor

```bash
conda activate pymor
pip install --isolated py-cmor[dev,fesom]
```

You can then check the Pymor works by running:

```bash
pymor --version
pymor --help
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
