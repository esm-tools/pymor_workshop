Running a basic pymor process
=============================

After everything is installed, it is time to CMORize our first dataset!

We will start by using example data from a fake atmosphere model and produce `tas` for `Amon`.

First, you'll need to write or modify the basic yaml file to load up that data. Open up a file
called `basic.yaml`, and add the following keys:
* `general`: this will hold settings for which cmor version is used
* `pymor`: this will hold settings for the pymor tool itself
* `rules`: this will be a list, defining which variables are processed
* `pipelines`: this will also be a list, defining which steps to take to process the data

Configure `pymor` to use:
* `CMIP6` settings
* One rule to process the model variable `"tsurf"` into the cmor variable `"tas"`
* Use the `Amon` table
* Files have the pattern "modelA_temp_????0101.nc", where ???? is a year stamp.

<details>
  <summary>Solution</summary>

  Here is how the yaml file could look like:

  ```yaml
  general:
    cmor_version: CMIP6
    CMIP_Tables_Dir: /work/ab0995/a270243/pymor_workshop/cmip6-cmor-tables/Tables/
    CV_Dir: /work/ab0995/a270243/pymor_workshop/cmip6-cmor-tables/CMIP6_CVs/
  pymor:
    warn_on_no_rule: False
    # dask_cluster: local
    # dask_cluster_scaling_mode: fixed
    # fixed_jobs: 1

  rules:
    - name: "linear trend example"
      cmor_variable: tas 
      experiment_id: "piControl"
      grid_label: "gn"
      model_component: "atmos"
      model_variable: tsurf
      output_directory: "."
      source_id: AWI-CM-1-1-HR
      table_name: "Amon"
      variant_label: "r1i1p1f1"
      inputs:
        - pattern: "modelA_temp_....0101.nc"
          path: "/work/ab0995/a270243/pymor_workshop/exercises/data"
  ```
</details>

Notice that we do not specify any pipelines in our configuration, so the default pipeline
is chosen. You can run the process with the following command:

```bash
$ pymor process basic.yaml
```

However, you should submit this to the SLURM scheduler, so instead:
```bash
$ sbatch pymor-basic.slurm
```

Note that you will need to modify the `pymor-basic.slurm` file to match your account!

<details>
  <summary>Solution</summary>
  
  ```diff
    #!/bin/bash -e
    #SBATCH --job-name=pymorize-controller  # <<< This is the main job, it will launch subjobs if you have Dask enabled.
  - #SBATCH --account=                      # <<< Adapt this to your computing account!
  + #SBATCH --account=<YOUR_ACCOUNT>        # <<< Adapt this to your computing account!
    #SBATCH --partition=compute
    #SBATCH --nodes=1
    #SBATCH --time=00:30:00                 # <<< You may need more time, adapt as needed!
  + clause for conda activate ...

  - cd /work/ab0246/a270077/SciComp/Projects/pymor-workshop/exercises/basic/
  + cd <YOUR_FOLDER>
    which pymor
    time pymor process basic.yaml 
  ```
</details>
