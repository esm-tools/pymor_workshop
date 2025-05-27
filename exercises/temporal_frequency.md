# Temporal frequency

One of the criteria to perform cmorization is that the temporal frequency of the source data must be **finer** than the frequency defined in the matching CMIP table.

For instance, if variable in source data matches monthly CMIP table, then it is required that source data temporal frequency is at least monthly. If it is coarser than monthly (say, quarterly or annual), then it is not possible to perform cmorization.

`Pymor` compares the temporal frequency of the source data with all matching CMIP tables frequencies and discards the ones which do not satisfy the above criteria from the pipeline.

---

Exercise folder: `temporal_frequency`


# Exercise

For this exercise, `CO2f` variable with quarterly temporal frequency is used.
As this variable maps to `fgco2` variable which is found in both monthly and yearly CMIP tables, Pymor should only consider yearly CMIP table for cmorization.

---

1. Using `cdo` for example, check the time stamps in the source files `../data/qCO2f_fesom_quaterly_*.nc`. What's the data frequency?

<details>
  <summary><b>Solution</b></summary>
  
```bash
$ cdo showdate ../data/qCO2f_fesom_quaterly_3001.nc
Warning (cdfScanVarAttr): NetCDF: Variable not found - time_bnds
  3001-01-01  3001-04-01  3001-07-01  3001-10-01
cdo    showdate: Processed 1 variable over 4 timesteps [0.03s 22MB].
```
The frequency of the source data is quarterly.
</details>

---

2. Check what should be the data frequency once the data is CMORised by looking at the yearly table for the variable `fgco2`.

<details>
  <summary><b>Solution</b></summary>

```bash
$ jq ".variable_entry.fgco2" ../cmip6-cmor-tables/Tables/CMIP6_Oyr.json
{
  "frequency": "yr",
  "modeling_realm": "ocnBgchem",
  "standard_name": "surface_downward_mass_flux_of_carbon_dioxide_expressed_as_carbon",
  "units": "kg m-2 s-1",
  "cell_methods": "area: mean where sea time: mean",
  "cell_measures": "area: areacello",
  "long_name": "Surface Downward Mass Flux of Carbon as CO2 [kgC m-2 s-1]",
  "comment": "Gas exchange flux of CO2 (positive into ocean)",
  "dimensions": "longitude latitude time",
  "out_name": "fgco2",
  "type": "real",
  "positive": "down",
  "valid_min": "",
  "valid_max": "",
  "ok_min_mean_abs": "",
  "ok_max_mean_abs": ""
}
```
The frequency of the CMORised data should be yearly (`"frequency": "yr"`) and is computed as a time mean.

</details>

---

3. Submit the job (`sbatch pymor.slurm`) and check the output. What is the time frequency of the new files?

<details>
  <summary><b>Solution</b></summary>
  
```bash
$ ls fgco2_Oyr*.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3001-3001.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3002-3002.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3003-3003.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3004-3004.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3005-3005.nc
```
  
```bash
$ cdo showdate fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3001-3001.nc
Warning (cdfScanVarAttr): NetCDF: Variable not found - time_bnds
  3001-01-01
cdo    showdate: Processed 1 variable over 1 timestep [0.02s 22MB].
```
Only one timestep is available, which is the result of making the mean over the whole year.

</details>

---

# Workflow

1. In terminal, change into `./temporal_frequency/` directory
2. Edit `temporal-frequency-example.yaml` file as necessary.
3. Submit the job to slurm scheduler. `sbatch pymor.slurm`
4. Check the output of the job.
