# Add a custom step in the pipeline

In this exercise, we will look into how to add a custom step to the pipeline.

Considering "Upward Ocean Mass Transport" dataset from `fesom` model.

The vertical velocity component 𝑤 (saved as ``wo`` in fesom) is scaled by the
cell area (`m2`) as well as a reference water density 𝜌0 = 1035 kg m−3.

So the task is to apply reference density to dataset. The cell area information is available in the griddes file.

The dimensions of the variables `wo` and `griddes.cell_area` are as follows:

  - `wo(time, nodes_3d=3668773)`
  - `griddes.cell_area(ncells=126859)`

As there is mismatch in dimensions, we need to transform `wo` to `(time, level, ncells)`. That is transforming the dimension `nodes_3d` to `(level, ncells=126859)`. This is done by `nodes_to_levels` function and it needs to be inserted into the pipeline.

The seconds step is to apply reference density per cell area to `wo`. This is done by `weight_by_cellarea_and_density` function and it needs to be inserted into the pipeline as well.

The `nodes_to_levels` and `weight_by_cellarea_and_density` functions are defined in `wo_cellarea.py` file.

The syntax to include custom functions in the pipeline is as follows:

`schema://<filepath>:<function_name>`

For example:

`script://wo_cellarea.py:nodes_to_levels`

`script://wo_cellarea.py:weight_by_cellarea_and_density`

---

Exercise folder: `custom_functions`

Exercise files:

- `wo_cellarea.yaml`
- `wo_cellarea.py`

# Exercise

1. Ensure `grid_file` and `mesh_path` parameters are set in `wo_cellarea.yaml` as they are required in computation inside custom functions.

  ```yaml
  grid_file: /pool/data/AWICM/FESOM1/MESHES/core/griddes.nc
  mesh_path: /pool/data/AWICM/FESOM1/MESHES/core
  ```

2. Ensure custom functions defined in `wo_cellarea.py` have the following signature:

  ```python
  def custom_function(data, rule):
      # do something with data and rule
      return data
  ```

3. Ensure these custom functions are inserted into the pipeline in `wo_cellarea.yaml`.

  ```yaml
  pipelines:
    - name: default
      steps:
        - "pymor.core.gather_inputs.load_mfdataset"
        - "pymor.std_lib.generic.get_variable"
        - "script://./wo_cellarea.py:nodes_to_levels"
        - "pymor.std_lib.timeaverage.compute_average"
        - "script://./wo_cellarea.py:weight_by_cellarea_and_density"
        - "pymor.std_lib.units.handle_unit_conversion"
        - "pymor.std_lib.setgrid.setgrid"
        - "pymor.std_lib.global_attributes.set_global_attributes"
        - "pymor.std_lib.generic.trigger_compute"
        - "pymor.std_lib.generic.show_data"
        - "pymor.std_lib.files.save_dataset"
  ```

### Note

To run this exercise fesom package is required. If you don't have it installed already, you can install it using `pip install py-cmor[fesom]`.

# Workflow

1. In terminal, navigate to the exercise folder `./custom_functions`.
2. Review or edit `wo_cellarea.yaml` file as necessary.
3. Submit the job using `sbatch pymorize_wo_cellarea.slurm`.


