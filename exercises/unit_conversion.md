# Unit conversion


After cmorization process the units in the output files are expected to match those defined in the CMIP tables.

When the units in the source files differ from the units in the CMIP tables, Pymor tool tries to handle the unit conversion automatically. It can also handle chemical names in the units (for example, moles of carbon). You, as a user, can also let Pymor know what are the units of your source data. This is useful to define units for variables that are incorrectly defined in the source files, or that are not recognised by the unit-conversion libraries used by Pymor.

The exercises covers the following topics:

- Handling chemical names in units in source files
- Handling incorrect units in source files

---

Exercise folder: `./unit_conversion`
Data folder: `./data`

The data used in the exercise are files matching pattern `CO2f_fesom_mon*.nc`. and `xCO2f_fesom_mon*.nc`.
The `CO2f` variable defined in these files, map to `fgco2` in CMIP tables (`Omon` table and `Oyr` table).

The units for `CO2f` variable is `mmolC/m2/d`. The units for `fgco2` in CMIP tables is `kg/m2/s`.

To simulate wrong units in source files, the units in files `xCO2f_fesom_mon*.nc` are set to `mol/m2/d`.
This means, we have tell Pymor tool the correct units by setting it in `unit_conversion/units-example.yaml` file. This is done by using the parameter `model_unit`.

# Exercise

1. Ensure correct units are defined in `unit_conversion/units-example.yaml` file.
   The following line should be added to the rule `xfgco2`.
   ```yaml
   model_unit: "mmolC/m2/d"
   ```

2. Grep the log file for unit conversion details.
   ```bash
   grep -i "molC" $(ls -rtd logs/pymor-process* | tail -n 1 )
   ```
   <details>
     <summary>Expected output</summary>

     ```bash
     | DEBUG    | pymor.std_lib.units:handle_chemicals:159 - Chemical element Carbon detected in units mmolC/m2/d.
     | DEBUG    | pymor.std_lib.units:handle_chemicals:160 - Registering definition: molC = 12.0107 * g
     ```
   </details>

3. Verify that the output files have correct units.
   ```bash
   ncdump -h fgco2_Omon_AWI-AWI-CM-1-1-HR_piControl_r1i1p1f1_gn_300101-300112.nc | grep units
   ```
   <details>
     <summary>Expected output</summary>

     ```bash
     units:                 kg m-2 s-1
     ```
   </details>
