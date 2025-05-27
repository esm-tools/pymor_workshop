# Using `pyfesom2` with `pymor`

In this exercise we will use `pyfesom2` functionality to regrid 
some data in a custom pipeline. `pymor` provides some `FESOM`-specific
features for dealing with model output, including things like regridding,
resetting node depths (for `FESOM` 1.x), and mesh aware calculations.

---

Exercise folder: `./pyfesom2`
Data folder: `./data`
Additionally needed: `./meshes/core2`

You can use the files with the pattern `CO2f_fesom_mon_.*nc`, as in previous exercises. To
start off, you'll need to define a pipeline that works for your regridding problem. You'll want
to include the following steps:

* Load up the data
* Extract the variable to go from `xr.Dataset` to `xr.DataArray`
* FESOM regridding
* Checkpoint before any calculations are done - dask will have already built up it's task graph
* Trigger computations
* Show data
* Dump data to a file on disk


<details>
  <summary>Solution</summary>

  Here is a pipeline snippet that does the above steps:
  ```yaml
  pipelines:
    - name: my-regridder
      steps:
        - pymor.core.gather_inputs.load_mfdataset
        - pymor.std_lib.generic.get_variable
        - pymor.fesom_2p1.regridding.regrid_to_regular
        - pymor.core.caching.manual_checkpoint
        - pymor.std_lib.generic.trigger_compute
        - pymor.std_lib.generic.show_data
        - pymor.std_lib.files.save_dataset
  ```

</details>

Next, you can fill out the `rules` section of your yaml as normal:

<details>
  <summary>Solution</summary>

  Load up the `CO2f` files and connect them to your pipeline:

  ```diff
  + rules:
  +   - name: CO2f_Regrid
  +     model_variable: CO2f
  +     cmor_variable: fgco2
  +     pipelines: [my-regridder]
  +     inputs:
  +        - path: /work/ab0995/a270243/pymor_workshop/data/
  +          pattern: CO2f_fesom_mon_300.0101.nc
  +     output_directory: "."
  +     # Metadata block
  +     experiment_id: "piControl"
  +     grid_label: "gn"
  +     model_component: "oce"
  +     source_id: "AWI-CM-1-1-HR"
  +     variant_label: "r1i1p1f1"
  pipelines:
    - name: my-regridder
      steps:
        - pymor.core.gather_inputs.load_mfdataset
        - pymor.std_lib.generic.get_variable
        - pymor.fesom_2p1.regridding.regrid_to_regular
        - pymor.core.caching.manual_checkpoint
        - pymor.std_lib.generic.trigger_compute
        - pymor.std_lib.generic.show_data
        - pymor.std_lib.files.save_dataset
  ```
</details>

Important for any bundled `pyfesom2` functionality is specifying where to 
find the mesh. You need to add `mesh_path` to your `rule` specifications:

<details>
  <summary>Solution</summary>

  Load up the `CO2f` files and connect them to your pipeline:

  ```diff
  rules:
    - name: CO2f_Regrid
      model_variable: CO2f
      cmor_variable: fgco2
      pipelines: [my-regridder]
      inputs:
         - path: /work/ab0995/a270243/pymor_workshop/data/
           pattern: CO2f_fesom_mon_300.0101.nc
      output_directory: "."
      # Metadata block
      experiment_id: "piControl"
      grid_label: "gn"
      model_component: "oce"
      source_id: "AWI-CM-1-1-HR"
      variant_label: "r1i1p1f1"
  +   mesh_path: /work/ab0246/a270077/SciComp/Projects/pymor-workshop/fesom-meshes/core/
  pipelines:
    - name: my-regridder
      steps:
        - pymor.core.gather_inputs.load_mfdataset
        - pymor.std_lib.generic.get_variable
        - pymor.fesom_2p1.regridding.regrid_to_regular
        - pymor.core.caching.manual_checkpoint
        - pymor.std_lib.generic.trigger_compute
        - pymor.std_lib.generic.show_data
        - pymor.std_lib.files.save_dataset
  ```
</details>
