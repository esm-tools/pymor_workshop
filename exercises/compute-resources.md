# Exercises: Customizing your Compute Resources

We want to do two things in this practice problem:

## 1. Switch from a `"local"` to `"slurm"`

<details>
  <summary>Solution</summary>
  In your YAML file, you can change the `pymor.dask_cluster`:

  ```yaml
  pymor:
    dask_cluster: "slurm"  # or "local"
  ```
</details>

Notice that when you specify `"slurm"`, you also need to have Dask's [`jobqueue`](https://jobqueue.dask.org) package configured. You
can do this in several ways:

* Job Level (easiest): Add a `jobqueue` block in your run configuration 
* User Level: Add a `~/.config/dask/jobqueue.yaml`
* System Level: Ask admins to add a `/etc/dask/jobqueue.yaml`

The [options](https://jobqueue.dask.org/en/latest/clusters-configuration-setup.html) for jobqueue can be found
in the handbook. The most important ones are:

```yaml
jobqueue:
  slurm:
    queue: <FILL IN>
    account: <FILL IN>
    cores: <FILL IN>  # Cores in the SLURM job (a SLURM job can have many Dask workers)
    memory: <FILL IN>
```

<details>
  <summary>Solution</summary>

  Here is a full setting list for `distributed` and `jobqueue`:

  ```yaml
  # Settings for using dask-distributed
  distributed:
    worker:
      memory:
        target: 0.6 # Target 60% of worker memory usage
        spill: 0.7 # Spill to disk when 70% of memory is used
        pause: 0.8 # Pause workers if memory usage exceeds 80%
        terminate: 0.95 # Terminate workers at 95% memory usage
      resources:
        CPU: 4 # Assign 4 CPUs per worker
      death-timeout: 600 # Worker timeout if no heartbeat (seconds): Keep workers alive for 5 minutes
  # SLURM-specific settings for launching workers
  jobqueue:
    slurm:
      name: pymorize-worker
      queue: compute # SLURM queue/partition to submit jobs
      account: ab0995 # SLURM project/account name
      cores: 4 # Number of cores per worker
      memory: 128GB # Memory per worker
      walltime: '00:30:00' # Maximum walltime per job
      interface: ib0 # Network interface for communication
      job-extra-directives: # Additional SLURM job options
        - '--exclusive' # Run on exclusive nodes
        - '--nodes=1'
      # Worker template
      worker-extra:
        - "--nthreads"
        - 4
        - "--memory-limit"
        - "128GB"
        - "--lifetime"
        - "25m"
        - "--lifetime-stagger"
        - "4m"
      # How to launch workers and scheduler
      job-cpu: 128
      job-mem: 256GB
      # worker-command: dask-worker
      processes: 32 # Limited by memory per worker!
      # scheduler-command: dask-scheduler
  ```

</details>


## 2. Increase the number of worker jobs `pymor` creates

<details>
  <summary>Solution</summary>

  You can change the number of jobs in your YAML file under `pymor.dask_cluster_scaling_fixed_jobs`:

  ```yaml
  pymor:
      dask_cluster_scaling_fixed_jobs: 8
  ```
</details>

## Additional Notes

If you want to test scalability of your workload, you can play with a few parameters:

* Number of `dask-worker` processes your SLURM jobs create.
* Total number of SLURM jobs to create
* Memory allowed for each `dask-worker`
* CPUs allowed for each `dask-worker`


