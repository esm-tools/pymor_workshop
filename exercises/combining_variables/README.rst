Multivariable Inputs and vertical integration
---------------------------------------------

Here we show how use two input variables and perform a
vertical integration. The motivating example is from the
``CMIP6_Omon.json`` table:

  .. code:: json

      "intpp": {
          "standard_name": "net_primary_mole_productivity_of_biomass_expressed_as_carbon_by_phytoplankton",
          "units": "mol m-2 s-1",
          "long_name": "Primary Organic Carbon Production by All Types of Phytoplankton",
          "comment": "Vertically integrated total primary (organic carbon) production by phytoplankton.  This should equal the sum of intpdiat+intpphymisc, but those individual components may be unavailable in some models.",
   }

In the ``AWI-ESM-1-REcoM`` case two phytoplanktion groups
contribute to primary production:

1. nanophytoplankton (variable ``diags3d01``)
2. diatoms (variable ``diags3d02``)

Hence, the workflow to get implemented would be:

.. math::

    \text{NPP} = \int_{\text{bottom}}^{\text{top}} (\text{NPP}_{\text{nanopythoplankton}} + \text{NPP}_{\text{diatoms}})

In pseudo-code::

  pp = diags3d01 + diags3d03
  pp.sum(dim="depth")
  mmol_mol = 1e-3
  per_day_to_per_sec = 1/86400
  conversion_factor_mmolC_m2_d_to_molC_m2_s = 1/1e3/86400  # About 1.157407e-08

We implement custom steps for the addition and vertical integration.

.. literalinclude:: ../examples/04-multivariable-input-with-vertical-integration/intpp_recom.py
   :linenos:
   :language: python

In your YAML file, you still need to include the script tags in the pipeline:

.. code-block::
  :linenos:
  :language: yaml

  pipelines:
    - name: default
      steps:
        - "pymor.core.gather_inputs.load_mfdataset"
        - "script://./intpp_recom.py:add_pp_components"
        - "pymor.fesom_1p4.nodes_to_levels"
        - "script://./intpp_recom.py:vertical_integration"
        - "script://./intpp_recom.py:set_pp_units"
        - "pymor.std_lib.convert_units"
        - "pymor.std_lib.time_average"
        - "pymor.std_lib.set_global_attributes"
        - "pymor.std_lib.trigger_compute"
        - "pymor.std_lib.show_data"
        - "pymor.std_lib.files.save_dataset"

You can submit this job with the provide slurm script!

