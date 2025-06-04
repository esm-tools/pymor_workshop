#!/usr/bin/env python3
"""
Creates fake data files from yaml specification

Usage
-----
Make sure you are in the same environment as you have for ``pymor``! Then, you
can run:

    $ python create-fake-data.py --yaml-file data-skeletons.yaml
"""
import os
import sys
from typing import Any, Dict

import numpy as np
import rich_click as click
import xarray as xr
import yaml
from rich import print


@click.command()
@click.option(
    "--yaml-file",
    "-y",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="YAML file specifying datasets to create",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    type=click.Path(file_okay=False),
    help="Directory to save generated files",
)
def main(yaml_file: str, output_dir: str) -> None:
    """Generate fake data files based on YAML specification."""
    print(f"[bold green]Generating fake data files from[/bold green] {yaml_file}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read YAML specification
    with open(yaml_file, "r") as f:
        try:
            spec = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[bold red]Error parsing YAML file:[/bold red] {e}")
            sys.exit(1)

    if not isinstance(spec, dict):
        print("[bold red]Error:[/bold red] YAML file must contain a dictionary")
        sys.exit(1)

    # Process each file specification
    for filename, dataset_spec in spec.items():
        try:
            # Create the dataset
            ds = create_dataset_from_spec(dataset_spec)

            # Save the dataset
            output_path = os.path.join(output_dir, filename)
            ds.to_netcdf(output_path)
            print(f"[bold green]Created[/bold green] {output_path}")
        except Exception as e:
            print(f"[bold red]Error creating {filename}:[/bold red] {e}")


def create_dataset_from_spec(spec: Dict[str, Any]) -> xr.Dataset:
    """Create an xarray Dataset based on the provided specification.

    Parameters
    ----------
    spec : Dict[str, Any]
        Dictionary containing the dataset specification

    Returns
    -------
    xr.Dataset
        The generated dataset with random data
    """
    # Extract dimensions
    dims = spec.get("dimensions", {})
    if not dims:
        raise ValueError("Dataset specification must include dimensions")

    # Create coordinates for each dimension
    coords = {}
    for dim_name, dim_spec in dims.items():
        if isinstance(dim_spec, int):
            # If dimension is just a size, create a simple index
            coords[dim_name] = np.arange(dim_spec)
        elif isinstance(dim_spec, dict):
            # If dimension has detailed specification
            size = dim_spec.get("size")
            if not size:
                raise ValueError(f"Dimension {dim_name} must specify a size")

            start = dim_spec.get("start", 0)
            step = dim_spec.get("step", 1)
            dtype = dim_spec.get("dtype", "float")

            if dtype.lower() in ["datetime", "date", "time"]:
                # Create datetime index
                start_date = dim_spec.get("start_date", "2000-01-01")
                freq = dim_spec.get("freq", "D")
                coords[dim_name] = xr.date_range(
                    start=str(start_date), periods=size, freq=freq, use_cftime=True
                )
            else:
                # Create numeric index
                end = start + (size * step)
                coords[dim_name] = np.arange(start, end, step)
        else:
            raise ValueError(f"Invalid dimension specification for {dim_name}")

    # Create data variables
    data_vars = {}
    variables = spec.get("variables", {})

    for var_name, var_spec in variables.items():
        # Get dimensions for this variable
        var_dims = var_spec.get("dimensions", list(dims.keys()))

        # Check that all dimensions exist
        for dim in var_dims:
            if dim not in coords:
                raise ValueError(f"Variable {var_name} uses undefined dimension {dim}")

        # Get shape for the variable
        shape = [len(coords[dim]) for dim in var_dims]

        # Generate random data based on distribution
        distribution = var_spec.get("distribution", "normal")
        data = generate_random_data(shape, distribution, var_spec)

        # Create the data variable
        attrs = var_spec.get("attrs", {})

        data_vars[var_name] = xr.DataArray(
            data=data, dims=var_dims, attrs=attrs, name=var_name
        )

    # Create the dataset
    ds = xr.Dataset(data_vars=data_vars, coords=coords)

    # Add global attributes if specified
    global_attrs = spec.get("global_attrs", {})
    ds.attrs.update(global_attrs)

    return ds


def generate_random_data(shape, distribution, var_spec):
    """Generate random data based on the specified distribution and parameters."""
    # Get distribution parameters
    params = var_spec.get("params", {})

    if distribution.lower() == "normal" or distribution.lower() == "gaussian":
        mean = params.get("mean", 0)
        std = params.get("std", 1)
        return np.random.normal(mean, std, shape)

    elif distribution.lower() == "uniform":
        low = params.get("low", 0)
        high = params.get("high", 1)
        return np.random.uniform(low, high, shape)

    elif distribution.lower() == "poisson":
        lam = params.get("lambda", 1)
        return np.random.poisson(lam, shape)

    elif distribution.lower() == "exponential":
        scale = params.get("scale", 1)
        return np.random.exponential(scale, shape)

    elif distribution.lower() == "constant":
        value = params.get("value", 0)
        return np.full(shape, value)

    else:
        raise ValueError(f"Unsupported distribution: {distribution}")


if __name__ == "__main__":
    # Fix missing pandas import
    import pandas as pd

    main()
