# Exercises: Using aux files

We want to explore auxiliary files in these exercises, which allow you to load up contextual information
alongside your data. 

```yaml
Exercise folder: aux_files
Exercise files: linear-trend.yaml, add_linear_trend.py, spatial-correction.yaml, spatial_correction.py
```

## 1. Aux files with a plain text file

In this example we will add a simple linear trend to ten years of data, and view the results using
`ncview`, to confirm that everything works fine. A practical use case here would be to add a varying
correction to your output data, which is different for each timestep and cannot be expressed purely
mathematically (you would use custom `script://` step for that case).

First, you'll create a text file with simple integers, one per line, counting up to 120. That is 
going to represent values of the increasing linear trend.

<details>
  <summary>Solution</summary>
  There are many ways to do this. For example:

  ```python
  numbers = list(range(1, 121))
  with open("numbers.txt", "w") as f:
      [f.write(f"{n}\n") for n in numbers]
  ```
  Or in pure shell:

  ```bash
  seq 1 120 > numbers.txt
  ```
</details>

Now, we will specify ten years of data in one of our rules. You can use 
the data from the basic example data here:

<details>
  <summary>Solution</summary>

  ```yaml
  general:
      cmor_version: CMIP6
  pymor:
      warn_on_no_rule: False
  rules:
      - name: "linear trend example"
        cmor_variable: tas 
        experiment_id: "piControl"
        grid_label: "gn"
        model_component: "atmos"
        model_variable: tsurf
        output_directory: "."
        source_id: "POOF-ESM"  # Paul's Outrageously Obviously Fake Earth System Model
        table_name: "Amon"
        variant_label: "r1i1p1f1"
        aux:
          - name: "numbers"
            path: "numbers.txt"
        inputs:
          - pattern: "modelA_temp_....0101.nc"
            path: "/work/ab0995/a270243/pymor_workshop/exercises/data"
        pipelines:
           - "linear_trend"
  ```
</details>

Also define the `linear_trend` pipeline.

<details>
  <summary>Solution</summary>

  ```yaml
  general:
      cmor_version: CMIP6
  pymor:
      warn_on_no_rule: False
  rules:
      - name: "linear trend example"
        cmor_variable: tas 
        experiment_id: "piControl"
        grid_label: "gn"
        model_component: "atmos"
        model_variable: tsurf
        output_directory: "."
        source_id: "POOF-ESM"  # Paul's Outrageously Obviously Fake Earth System Model
        table_name: "Amon"
        variant_label: "r1i1p1f1"
        aux:
          - name: "numbers"
            path: "numbers.txt"
        inputs:
          - pattern: "modelA_temp_....0101.nc"
            path: "/work/ab0995/a270243/pymor_workshop/exercises/data"
        pipelines:
           - "linear_trend"
  pipelines:
      - name: "linear_trend"
        steps:
          - "pymor.core.gather_inputs.load_mfdataset"
          - "pymor.std_lib.generic.get_variable"
          - "script://add_linear_trend.py:add_linear_trend"
          - "pymor.std_lib.generic.trigger_compute"
          - "pymor.std_lib.generic.show_data"
          - "pymor.std_lib.files.save_dataset"
   ```


</details>

Your YAML file should now be ready. You'll also need to write the script
with your custom step:
    
<details>
  <summary>Solution</summary>

  ```python
  import xarray as xr


  def add_linear_trend(data, rule):
      numbers = rule.aux["numbers"]
      numbers = [int(n) for n in numbers.split()]
      # Convert the numbers into an xarray with timestamps:
      numbers = xr.DataArray(data=numbers, coords=[data.time])
      data += numbers
      data.name = "example"
      return data
  ```
</details>

Next, you can submit your job:

<details>
  <summary>Solution</summary>
  
  ```console
  $ sbatch exercises/aux_files/linear-trend.slurm
  ```
</details>

## 2. Use a NetCDF File to add a spatial-varying offset

Here, we want to some form of correction to our data, varying in space. First, you'll
need to create a random field to add to your data, representing your correction. You can
use `cdo` for that.

<details>
  <summary>Solution</summary>
  
  ```console
  $ cdo -f nc -mulc,100 -random,r720x360 my_correction.nc 
  ```
</details>

You can adapt the `pymor` configuration from before, this time specifying your field as 
an offset. You'll also need to create a new custom step script, and make sure that your
new aux file can be read in correctly.

<details>
  <summary>Solution</summary>

  You'll need to take care of a few things here:

  1. Specifying the new aux file

  ```diff
    aux:
  -    - name: "numbers"
  -      path: "numbers.txt"
  +    - name: "spatial-correction"
  +      path: "my_correction.nc"
  +      loader: "xarray.open_dataset"
  ```

</details>
