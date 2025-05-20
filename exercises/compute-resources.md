# Exercises: Customizing your Compute Resources

We want to do two things in this practice problem:

1. Switch from SLURM to local (or the other way around)

<details>
    <summary>Solution</summary>
    In your YAML file, you can change the `pymor.dask_cluster` to either `slurm` or `local`:

    ```yaml
    pymor:
        dask_cluster: "slurm"  # or "local"
    ```
</details>


2. Increase the number of worker jobs `pymor` creates

<details>
    <summary>Solution</summary>

    You can change the number of jobs in your YAML file under `pymor.fixed_jobs`:

    ```yaml
    pymor:
        fixed_jobs: 8
    ```
<details>
