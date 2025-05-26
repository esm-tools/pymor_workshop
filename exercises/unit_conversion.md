# Unit conversion


After cmorization process the units in the output files are expected to match
those defined in the CMIP tables.

When the units in the source files differ from the units in the CMIP tables,
Pymor tool tries to handle the unit conversion automatically. It can also handle
chemical names in the units (for example, moles of carbon). You, as a user, can
also let Pymor know what are the units of your source data. This is useful to
define units for variables that are incorrectly defined in the source files, or
that are not recognised by the unit-conversion libraries used by Pymor.

The exercises covers the following topics:

- Handling chemical names in units in source files
- Handling incorrect units in source files
- Adding aliases in dimensionless_mapping.yaml file

---

# Exercise 1: Chemical name in units

Exercise folder: `./unit_conversion`
Exercise files: `./unit_conversion/units-example.yaml`, `./unit_conversion/units-example.slurm` 
Data: `./data/CO2f_fesom_mon*.nc`

The `CO2f` variable defined in these files, map to `fgco2` in CMIP tables (`Omon` table and `Oyr` table).
The units for `CO2f` is `mmolC/m2/d`.  The units for `fgco2` in CMIP tables is `kg/m2/s`.

1. Task: Verify the units in data and in tables by executing the following commands

  ```bash
  # change directory to exercise folder
  cd /work/$(id -gn)/$USER/pymor_workshop/exercise
  
  # grep for units in source file
  ncdump -h data/CO2f_fesom_mon_30010101.nc | grep units
  
  # units defined in CMIP6_Omon table
  jq '.variable_entry.fgco2.units' ../cmip6-cmor-tables/Tables/CMIP6_Omon.json 
  
  # units defined in CMIP6_Oyr table
  jq '.variable_entry.fgco2.units' ../cmip6-cmor-tables/Tables/CMIP6_Oyr.json 
  ```

As Pymor can understand unit `molC` and can convert to `kg`, the next step submit the job.

2. Task: submit the job

  ```bash
  cd unit_conversion
  sbatch units-example.slurm
  ```

3. Task: Verify the units in cmorized data


# Exercise 2: Incorrect units in source files

Exercise folder: `./unit_conversion`
Exercise files: `./unit_conversion/incorrect_units.yaml`, `./unit_conversion/incorrect_units.slurm` 
Data: `./data/xCO2f_fesom_mon*.nc`


To simulate incorrect units (units that cannot be interpreted by Pymor) in
source files, the units in files `xCO2f_fesom_mon*.nc` are set to
`mol/m2/d`. These units are "incorrect" because Pymor needs to be made aware of
the chemical composition before it can automatically convert moles to `kg`.
This means, we have tell Pymor tool the correct units by setting it in
`unit_conversion/incorrect_units.yaml` file. This is done by using the parameter
`model_unit`.

1. Task: check the units in source file

  ```bash
  # change directory to exercise folder
  cd /work/$(id -gn)/$USER/pymor_workshop/exercise
  
  # grep for units in source file
  ncdump -h data/xCO2f_fesom_mon_30060101.nc | grep units
  ```

2. Add correct units are defined in `unit_conversion/incorrect_units.yaml` file.
   ```yaml
   model_unit: "mmolC/m2/d"
   ```
   <details>
     <summary>Solution</summary>

     ```yaml
     rules:
     # Example showing wrong units in source data files.
       - name: xfgco2
         [ ... ]
         # UNITS IN DATA FILE ARE WRONG.
         # PROVIDE CORRECT UNITS USING `model_unit` parameter.
         # UNITS to set "mmolC/m2/d"
         model_unit: "mmolC/m2/d"
         [ ... ]
     ```
   </details>

2. Task: Submit the compute job

  ```bash
  cd unit_conversion
  sbatch incorrect_units.slurm
  ```

3. Task: Once the job is finished, grep the log file for unit conversion details.
   ```bash
   grep -i "mmolC" $(ls -rtd logs/pymor-process* | tail -n 1 )
   ```
   <details>
     <summary>Expected output</summary>

     ```bash
     | DEBUG    | pymor.std_lib.units:handle_chemicals:159 - Chemical element Carbon detected in units mmolC/m2/d.
     | DEBUG    | pymor.std_lib.units:handle_chemicals:160 - Registering definition: molC = 12.0107 * g
     ```
   </details>

4. Verify that the output files have correct units.
   ```bash
   ncdump -h fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300112.nc | grep units
   ```
   <details>
     <summary>Expected output</summary>

     ```bash
     units:                 kg m-2 s-1
     ```
   </details>


# Exercise 3: dimensionless mapping

TODO
