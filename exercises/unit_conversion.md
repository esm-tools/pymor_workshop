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

```yaml
EXERCISE FOLDER: unit_conversion
EXERCISE FILES: units-example.yaml, units-example.slurm
DATA: CO2f_fesom_mon*.nc
```

The `CO2f` variable defined in these files, map to `fgco2` in CMIP tables (`Omon` table and `Oyr` table).
The units for `CO2f` is `mmolC/m2/d`.  The units for `fgco2` in CMIP tables is `kg/m2/s`.

  1. TASK: Verify the units in data and in tables by executing the following commands

  ```bash
  # change directory to exercise folder
  cd /work/$(id -gn)/$USER/pymor_workshop/exercise
  
  # grep for units in source file
  ncdump -h data/CO2f_fesom_mon_30010101.nc | grep units
  ```
  
  <details>
    <summary>Expected output</summary>
    
  ```shell
    time:units = "seconds since 3001-01-01 0:0:0" ;
    CO2f:units = "mmolC/m2/d" ;
  ```
  </details>

---

  2. TASK: Verify the units in CMIP tables

  ```bash
  # units defined in CMIP6_Omon table
  jq '.variable_entry.fgco2.units' ../cmip6-cmor-tables/Tables/CMIP6_Omon.json 
  
  # units defined in CMIP6_Oyr table
  jq '.variable_entry.fgco2.units' ../cmip6-cmor-tables/Tables/CMIP6_Oyr.json 
  ```

  <details>
    <summary>Expected output</summary>
    
  ```shell
    "kg m-2 s-1"
  ```
  </details>

---

  3. TASK: submit the job

As Pymor can understand unit `molC` and can convert to `kg`, the next step submit the job.

  ```bash
  cd unit_conversion
  sbatch units-example.slurm
  ```

---

  4. TASK: Verify the units in cmorized data

  ```bash
  ncdump -h fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300112.nc | grep units
  ```

  <details>
    <summary>Expected output</summary>
    
  ```shell
    units:                 kg m-2 s-1
  ```
  </details>

---

# Exercise 2: Incorrect units in source files

```yaml
EXERCISE FOLDER: unit_conversion
EXERCISE FILES: incorrect_units.yaml, incorrect_units.slurm
DATA: xCO2f_fesom_mon*.nc
```

To simulate incorrect units (units that cannot be interpreted by Pymor) in
source files, the units in files `xCO2f_fesom_mon*.nc` are set to
`mol/m2/d`. These units are "incorrect" because Pymor needs to be made aware of
the chemical composition before it can automatically convert moles to `kg`.
This means, we have tell Pymor tool the correct units by setting it in
`incorrect_units.yaml` file. This is done by using the parameter
`model_unit`.

---

  1. TASK: check the units in source file

  ```bash
  # change directory to exercise folder
  cd /work/$(id -gn)/$USER/pymor_workshop/exercise
  
  # grep for units in source file
  ncdump -h data/xCO2f_fesom_mon_30060101.nc | grep units
  ```

  <details>
    <summary>Expected output</summary>
    
  ```shell
    time:units = "seconds since 3006-01-01 0:0:0" ;
    xCO2f:units = "mol/m2/d" ;
  ```
  </details>

---

  2. TASK: Add correct units are defined in `incorrect_units.yaml` file.
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

---

  3. TASK: Submit the compute job

  ```bash
  cd unit_conversion
  sbatch incorrect_units.slurm
  ```

---

  4. TASK: Once the job is finished, grep the log file for unit conversion details.
  
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

---

  5. TASK: Verify that the output files have correct units.
  
   ```bash
   ncdump -h fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300112.nc | grep units
   ```
   
   <details>
     <summary>Expected output</summary>

     ```bash
     units:                 kg m-2 s-1
     ```
   </details>

---

# Exercise 3: dimensionless mapping


For providing an alias for dimensionless-units, use parameter
`dimensionless_mapping_table` to set the unit mappings on the rule. The value
for this parameter is a yaml file mapping the original unit to an alias unit.

---

1. TASK: List dimensionless units in CMIP6 monthly table

   ```bash
   # change directory to exercise folder
   cd /work/$(id -gn)/$USER/pymor_workshop/exercise

   jq -r '.variable_entry | to_entries[] | select(.value.units | test("^\\d+(\\.\\d+)?$")) | "\(.value.out_name)\t\(.value.units)"' ../cmip6-cmor-tables/Tables/CMIP6_Omon.json | column -t
   ```

   <details>
     <summary>Expected output</summary>

     ```bash
     limfecalc   1
     limfediat   1
     limfediaz   1
     limfemisc   1
     limfepico   1
     limirrcalc  1
     limirrdiat  1
     limirrdiaz  1
     limirrmisc  1
     limirrpico  1
     limncalc    1
     limndiat    1
     limndiaz    1
     limnmisc    1
     limnpico    1
     ph          1
     phabio      1
     phabioos    1
     phnat       1
     phnatos     1
     phos        1
     so          0.001
     sob         0.001
     soga        0.001
     sos         0.001
     sosga       0.001
     ```
   </details>

---

2. TASK: List sort of vague/ambigious dimensions in CMIP6 montly table

   ```bash
   jq -r '.variable_entry | to_entries[] | select(.value.units | contains("mol")) | "\(.value.out_name)\t\(.value.units)"' ../cmip6-cmor-tables/Tables/CMIP6_Omon.json | column -t
   ```
   
   <details>
     <summary>Expected output</summary>
     
     Units just having `mol` does not tell which Element it is reffering to.
     These are potential candidates to include in dimensionless mapping table.

     ```bash
     arag            mol  m-3
     aragos          mol  m-3
     bacc            mol  m-3
     baccos          mol  m-3
     bfe             mol  m-3
     bfeos           mol  m-3
     bsi             mol  m-3
     bsios           mol  m-3
     calc            mol  m-3
     calcos          mol  m-3
     cfc11           mol  m-3
     cfc12           mol  m-3
     co3             mol  m-3
     co3abio         mol  m-3
     co3abioos       mol  m-3
     co3nat          mol  m-3
     co3natos        mol  m-3
     co3os           mol  m-3
     co3satarag      mol  m-3
     co3sataragos    mol  m-3
     co3satcalc      mol  m-3
     co3satcalcos    mol  m-3
     detoc           mol  m-3
     detocos         mol  m-3
     dfe             mol  m-3
     dfeos           mol  m-3
     dissi13c        mol  m-3
     dissi13cos      mol  m-3
     dissi14cabio    mol  m-3
     dissi14cabioos  mol  m-3
     dissic          mol  m-3
     dissicabio      mol  m-3
     dissicabioos    mol  m-3
     dissicnat       mol  m-3
     dissicnatos     mol  m-3
     dissicos        mol  m-3
     dissoc          mol  m-3
     dissocos        mol  m-3
     dmso            mol  m-3
     dmsos           mol  m-3
     eparag100       mol  m-2  s-1
     epc100          mol  m-2  s-1
     epcalc100       mol  m-2  s-1
     epfe100         mol  m-2  s-1
     epn100          mol  m-2  s-1
     epp100          mol  m-2  s-1
     epsi100         mol  m-2  s-1
     expc            mol  m-2  s-1
     fbddtalk        mol  m-2  s-1
     fbddtdic        mol  m-2  s-1
     fbddtdife       mol  m-2  s-1
     fbddtdin        mol  m-2  s-1
     fbddtdip        mol  m-2  s-1
     fbddtdisi       mol  m-2  s-1
     fddtalk         mol  m-2  s-1
     fddtdic         mol  m-2  s-1
     fddtdife        mol  m-2  s-1
     fddtdin         mol  m-2  s-1
     fddtdip         mol  m-2  s-1
     fddtdisi        mol  m-2  s-1
     fgcfc11         mol  m-2  s-1
     fgcfc12         mol  m-2  s-1
     fgdms           mol  m-2  s-1
     fgo2            mol  m-2  s-1
     fgsf6           mol  m-2  s-1
     frfe            mol  m-2  s-1
     fric            mol  m-2  s-1
     frn             mol  m-2  s-1
     froc            mol  m-2  s-1
     fsfe            mol  m-2  s-1
     fsn             mol  m-2  s-1
     graz            mol  m-3  s-1
     icfriver        mol  m-2  s-1
     intparag        mol  m-2  s-1
     intpbfe         mol  m-2  s-1
     intpbn          mol  m-2  s-1
     intpbp          mol  m-2  s-1
     intpbsi         mol  m-2  s-1
     intpcalcite     mol  m-2  s-1
     intpn2          mol  m-2  s-1
     intpp           mol  m-2  s-1
     intppcalc       mol  m-2  s-1
     intppdiat       mol  m-2  s-1
     intppdiaz       mol  m-2  s-1
     intppmisc       mol  m-2  s-1
     intppnitrate    mol  m-2  s-1
     intpppico       mol  m-2  s-1
     nh4             mol  m-3
     nh4os           mol  m-3
     no3             mol  m-3
     no3os           mol  m-3
     o2              mol  m-3
     o2min           mol  m-3
     o2os            mol  m-3
     o2sat           mol  m-3
     o2satos         mol  m-3
     ocfriver        mol  m-2  s-1
     phyc            mol  m-3
     phycalc         mol  m-3
     phycalcos       mol  m-3
     phycos          mol  m-3
     phydiat         mol  m-3
     phydiatos       mol  m-3
     phydiaz         mol  m-3
     phydiazos       mol  m-3
     phyfe           mol  m-3
     phyfeos         mol  m-3
     phymisc         mol  m-3
     phymiscos       mol  m-3
     phyn            mol  m-3
     phynos          mol  m-3
     phyp            mol  m-3
     phypico         mol  m-3
     phypicoos       mol  m-3
     phypos          mol  m-3
     physi           mol  m-3
     physios         mol  m-3
     po4             mol  m-3
     po4os           mol  m-3
     pon             mol  m-3
     ponos           mol  m-3
     pop             mol  m-3
     popos           mol  m-3
     pp              mol  m-3  s-1
     ppos            mol  m-3  s-1
     sf6             mol  m-3
     si              mol  m-3
     sios            mol  m-3
     talk            mol  m-3
     talknat         mol  m-3
     talknatos       mol  m-3
     talkos          mol  m-3
     zmeso           mol  m-3
     zmesoos         mol  m-3
     zmicro          mol  m-3
     zmicroos        mol  m-3
     zmisc           mol  m-3
     zmiscos         mol  m-3
     zooc            mol  m-3
     zoocos          mol  m-3
     ```
   </details>
   
---

3. TASK: Explore the dimensionless mapping table included in Pymor.

   ```bash
   filepath=$(python -c "import pathlib; import pymor.data; print(str(pathlib.Path(pymor.data.__file__).parent) + '/dimensionless_mappings.yaml')")
   
   echo $filepath
   cat $filepath
   ```
   
   Notice that very few fields (`sea_surface_salinity`) are pre-populated with
   aliases.  If your variable is not in pre-poulated fields, Pymor complains
   about unit conversion.
   
   To fill in missing entries, either modify this file or provide a new yaml
   file with only entries that care about using `dimensionless_mapping_table`
   parameter.
   
   To make newly added entries available for everyone, please create a
   PullRequest using the modified built-in mapping table.

   NOTE: It is **not** expected from you to create a PullRequest during
   the workshop as a task to perform.
  
   Additional notes: https://pymorize.readthedocs.io/en/latest/cookbook.html#working-with-dimensionless-units
   
---

4. TASK: Setting the dimensionless mapping

```yaml
EXERCISE FOLDER: unit_conversion
EXERCISE FILES: dimensionless_units.yaml, dimensionless_units.slurm, dimensionless_table.yaml
DATA: so_fesom_mon*.nc
```

  - units defined in source files
  
    ```bash
    ncdump -h ../data/so_fesom_mon_30010101.nc | grep units
    ```
    
    <details>
      <summary>Expected output</summary>
      
      ```bash
		time:units = "seconds since 3001-01-01 0:0:0" ;
		so:units = "psu" ;
      ```
    </details>

    Units `psu` means `pratical salinity units`. 

---

  - units found in tables
  
    ```bash
    jq '.variable_entry.so.units' ../cmip6-cmor-tables/Tables/CMIP6_Omon.json
    ```
    
    <details>
      <summary>Expected output</summary>
      
      ```bash
      0.001
      ```
    </details>
    
---

  - The dimensionless unit `0.001` can be expressed as `g/kg` to indicate `psu`.
    This mapping is already built-in into Pymor but here we want to explicitly use this mapping in cmorization process.
    
    ```bash
    cd unit_conversion
    cat dimensionless_table.yaml
    ```
    
    contents:
    ```bash
    so:
      "0.001": g/kg
    ```

  - Add table entry to `dimensionless_units.yaml` file in `pymor` section.
    Note: This is not a per-rule setting. This is for whole process.
  
    The entry must be `dimensionless_mapping_table: dimensionless_table.yaml`

    <details>
      <summary>Solution</summary>
    
    ```yaml
    [...]
    pymor:
      dimensionless_mapping_table: dimensionless_table.yaml
    [...]
    ```
    </details> 

---

  - Submit the job
  
  ```bash
  sbatch dimensionless_units.slurm
  ```
  
---

5. TASK: Verify the units in the output files.

  The units must be `0.001`

---
