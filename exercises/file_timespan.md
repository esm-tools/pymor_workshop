# File timespan

`file_timespan` parameter controls how many time steps are packed into a single file.
The default behavior is follow the same timespan as the input files. That means the same number of output files are generated as input files.

example options for this parameter: `6MS`, `1YS`, `10YS`
alternatively, these can also be expressed in days: `180D`, `365D`, `3650D`

---

Exercise folder: `./file_timespan`
Data folder: `./data`

The data used in the exercise are files with the pattern `CO2f_fesom_mon_.*nc`.
These files have a monthly frequency data and a year worth of time steps are packed into each file.

The `CO2f` variable maps to `fgco2` in CMOR table. `fgco2` is found in `Omon` and `Oyr` tables. So expected output files to be cmorized for both tables.

Here is the output without  providing `file_timespan` parameter:

```bash
file-timespan: None, table_id: None

  fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300112.nc
  fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300201-300212.nc
  fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300301-300312.nc
  fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300401-300412.nc
  fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3001-3001.nc
  fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3002-3002.nc
  fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3003-3003.nc
  fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3004-3004.nc
```

# Exercise

1. set `file_timespan` to `2YS` and `table_id` to `Omon` and run the job

   How many files are expected in the output?
   Guess the timestamp ranges in the file name.

   <details>
    <summary>Solution</summary>

    Set the following in `file-timespan-example.yaml```
    ```yaml
    rules:
      - name: fgco2
        [ ... ]
        file_timespan: "2YS"
        table_id: Omon
        [ ... ]
    ```

    After running pymor the following files should have been created:
    ```bash
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300212.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300301-300412.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300501-300512.nc
    ```

  </details>

2. set `file_timespan` to `6MS` and `table_id` to `Omon` and run the job

   How many files are expected in the output?
   Guess the timestamp ranges in the file name.

   <details>
    <summary>Solution</summary>

    ```bash
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300106.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300107-300112.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300201-300206.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300207-300212.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300301-300306.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300307-300312.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300401-300406.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300407-300412.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300501-300506.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300507-300512.nc
    ```

   </details>

3. set `file_timespan` to `6MS` and `table_id` to `None` and run the job

   With `table_id` set to `None`, we expect cmorized data w.r.t `Oyr` table to be generated as well.
   What is the expected time split of these files?
   
   <details>
    <summary>Solution</summary>

    ```bash
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300106.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300107-300112.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300201-300206.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300207-300212.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300301-300306.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300307-300312.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300401-300406.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300407-300412.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300501-300506.nc
    fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300507-300512.nc
    fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3001-3001.nc
    fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3002-3002.nc
    fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3003-3003.nc
    fgco2_Oyr_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_3004-3004.nc
    ```

   </details>

4. How to get a single output file?

   What should be the value of `file_timespan` to get a single output file?

   <details>
    <summary>Solution</summary>

   The value of `file_timespan` should be large enough to include all time steps.

    ```yaml
        file_timespan: 10YS
    ```
   
   Setting `file_timespan` to some value requires a bit of knowlege of time-span of source data.
   
   An alternative approach is to have keyword like `single_file` that `file_timespan` can accept.
   If you need such a feature, please raise an issue on github or better yet, submit a pull request.
   </details>

# Workflow

1. In terminal, change into `./file_timespan/` directory
2. Edit `file-timespan-example.yaml` file as necessary.
3. Submit the job to slurm schedular. `sbatch pymor.slurm`
