# Exercises: Using aux files

We want to explore auxiliary files in these exercises, which allow you to load up contextual information
alongside your data. 

## 1. Aux files with a plain text file

In this example we will add a simple linear trend to ten years of data, and view the results using
`ncview`, to confirm that everything works fine. A practical use case here would be to add a varying
correction to your output data, which is different for each timestep and cannot be expressed purely
mathematically (you would use custom `script://` step for that case).

First, you'll create a text file with simple integers, one per line, counting up to 120

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

Now, we will specify ten years of data in one of our rules. You can use any data you want here:

<details>
  <summary>Solution</summary>

  ```yaml
  general:
      cmor_version: CMIP6
  pymor:
      warn_on_no_rule: False
  rules:
      - name: "linear trend example"
        inputs:
          - pattern: "wo_fesom_....0101.nc"
            path: "/work/ab0995/a270243/pymor_workshop/exercises/data"
        aux:
          - name: "numbers"
            path: "numbers.txt"
        pipelines:
           - "linear_trend"
  ```
</details>

Finally, define the `linear_trend` pipeline. 

<details>
  <summary>Solution</summary>

  ```yaml
  general:
      cmor_version: CMIP6
  pymor:
      warn_on_no_rule: False
  rules:
      - name: "linear trend example"
        inputs:
          - path: "."
            pattern: "???"
        aux:
          - name: "numbers"
            path: "numbers.txt"
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



Your YAML file should now be ready. You'll also need to write the script with your custom step:

    
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


Next, we add the aux files to the rule:
<details>
  <summary>Solution</summary>

  ```yaml
  rules:
      - name: "linear trend example"
        inputs:
          - path: "."
            pattern: "???"
        aux:
          - name: "numbers"
            path: "numbers.txt"
        pipelines:
           - "linear_trend"
  ```


</details>

