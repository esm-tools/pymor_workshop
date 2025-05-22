# Adjust timestamp

Pymor provides `adjust_timestamp` parameter to adjust the timestamps in the cmorized datasets.

Possible values this parameter accepts:

  - named arguments: `first`, `last`, `mid`
  - floating number: between `0.0` and `1.0`
  - Literal offset: `14D`, `30D`
 
If `adjust_timestamp` is not provided in the yaml file, the default is `first`.

The floating number represents the offset as scaled values for `approx_interval` defined in the CMIP table.

---

For the exercise, we wanna see how this parameter influences the timestamps.

Exercise folder: `./adjust_timestamp`

Data used in the exercise has the following timestamps

```shell
cdo -s showtimestamp ../data/CO2f_fesom_mon_30010101.nc | xargs -n1 echo
3001-01-16T23:59:59
3001-02-15T11:59:59
3001-03-16T23:59:59
3001-04-16T11:59:59
3001-05-16T23:59:59
3001-06-16T11:59:59
3001-07-16T23:59:59
3001-08-16T23:59:59
3001-09-16T11:59:59
3001-10-16T23:59:59
3001-11-16T11:59:59
3001-12-16T23:59:59
```


# Exercise


1. To get middle-of-the-month timestamps in the cmorized data, what value is used for `adjust_timestamp`

   Is it `mid` or `14D`? Try with both of them.

   <details>
      <summary>Solution</summary>
  
      - setting `adjust_timestamp: mid`, timestamps look like this:
      ```shell
      3001-01-15T12:00:00
      3001-02-14T00:00:00
      3001-03-15T12:00:00
      3001-04-15T00:00:00
      3001-05-15T12:00:00
      3001-06-15T00:00:00
      3001-07-15T12:00:00
      3001-08-15T12:00:00
      3001-09-15T00:00:00
      3001-10-15T12:00:00
      3001-11-15T00:00:00
      3001-12-15T12:00:00
      ```
  
      - setting `adjust_timestamp: 14D`, timestamps look like this:
      ```shell
      3001-01-15T00:00:00
      3001-02-15T00:00:00
      3001-03-15T00:00:00
      3001-04-15T00:00:00
      3001-05-15T00:00:00
      3001-06-15T00:00:00
      3001-07-15T00:00:00
      3001-08-15T00:00:00
      3001-09-15T00:00:00
      3001-10-15T00:00:00
      3001-11-15T00:00:00
      3001-12-15T00:00:00
      ```

   </details>

2. If `adjust_timestamp` is ommited from yaml file, how does the timestamps look like in the cmorized data?
 
   <details>
      <summary>Solution</summary>

      - timestamps look as follows:
      ```shell
      3001-01-01T00:00:00
      3001-02-01T00:00:00
      3001-03-01T00:00:00
      3001-04-01T00:00:00
      3001-05-01T00:00:00
      3001-06-01T00:00:00
      3001-07-01T00:00:00
      3001-08-01T00:00:00
      3001-09-01T00:00:00
      3001-10-01T00:00:00
      3001-11-01T00:00:00
      3001-12-01T00:00:00
      ```
      
   </details>

# Workflow

1. In terminal, change into `./adjust_timestamp/` directory
2. Edit `adjust-timestamp-example.yaml` file as necessary.
3. Submit the job to slurm scheduler. `sbatch pymorize.slurm`
4. Load `cdo` into environment (if not already loaded) `module load cdo`
5. Use `cdo` to investigate the timestamp in a file `cdo -s showtimestamp <filename>.nc`
