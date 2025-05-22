# Temporal frequency

One of the criteria to perform cmorization is that the temporal frequency of the source data must be **finer** than the frequency defined in the matching CMIP table.

For instance, if variable in source data matches monthly CMIP table, then it is required that source data temporal frequency is at least monthly. If it is coarser than monthly (say, quarterly or annual), then it is not possible to perform cmorization.

`Pymor` compares the temporal frequency of the source data with all matching CMIP tables frequencies and discards the ones which do not satisfy the above criteria from the pipeline.

---

Exercise folder: `temporal_frequency`


# Exercise

For this exercise, `CO2f` variable with quarterly temporal frequency is used.
As this variable maps to `fgco2` variable which is found in both monthly and yearly CMIP tables, Pymor should only consider yearly CMIP table for cmorization.

submit the job (`sbatch pymorize.slurm`) and check the output

```bash
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3001-3001.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3002-3002.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3003-3003.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3004-3004.nc
fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3005-3005.nc
```

# Workflow

1. In terminal, change into `./temporal_frequency/` directory
2. Edit `temporal-frequency-example.yaml` file as necessary.
3. Submit the job to slurm scheduler. `sbatch pymorize.slurm`
4. Check the output of the job.
