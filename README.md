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
