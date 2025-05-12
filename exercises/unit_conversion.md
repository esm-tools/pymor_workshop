# Unit conversion


After cmorization process the units in the output files are expected to as defined in the CMIP tables.

When the units in the source files differ from the units in the CMIP tables, Pymor tool handles the unit conversion automatically almost all the time. It can also handle chemical names in the units. It also support alternative source of defining units. This can be used to define units for variables that are incorrectly defined in the source files.

The exercises covers the following topics:

- Chemical names in units
- Alternative source of defining units

The data for the exercises is available in the `data` directory.

The `CO2f` variable is defined source files (`CO2f_fesom_mon*.nc`) with units `mmolC/m2/d` maps to `fgco2` in the CMIP tables as `kg/m2/d`.

To simulate wrong units in source files, the units in files `xCO2f_fesom_mon*.nc` are set to `mol/m2/d`. To correct units are defined in the `unit_conversion/units-example.yaml`

