#!/usr/bin/env python3
"""
Creates a YAML skeleton from an existing NetCDF file.

This script analyzes a NetCDF file and produces a YAML specification that
can be used with create-fake-data.py to generate similar synthetic data.

Usage
-----
Make sure you are in the same environment as you have for ``pymor``! Then, you
can run:

    $ python netcdf-to-yaml.py --netcdf-file input.nc --yaml-file output.yaml
"""
import os
import sys
from datetime import datetime
import numpy as np
import xarray as xr
import rich_click as click
from rich import print
import ruamel.yaml

# Use ruamel.yaml for better formatting control
yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 80
yaml.preserve_quotes = True


@click.command()
@click.option(
    "--netcdf-file",
    "-n",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="NetCDF file to analyze",
)
@click.option(
    "--yaml-file",
    "-y",
    required=False,
    type=click.Path(writable=True, dir_okay=False),
    help="Output YAML file (defaults to <netcdf_filename>.yaml)",
)
@click.option(
    "--output-filename",
    "-o",
    required=False,
    help="Filename to use in the YAML spec (defaults to input filename)",
)
def main(netcdf_file, yaml_file, output_filename):
    """Generate a YAML skeleton from a NetCDF file."""
    print(f"[bold green]Analyzing NetCDF file:[/bold green] {netcdf_file}")
    
    # Set default output filename if not provided
    if not yaml_file:
        base_name = os.path.splitext(netcdf_file)[0]
        yaml_file = f"{base_name}.yaml"
    
    # Set default output_filename if not provided
    if not output_filename:
        output_filename = os.path.basename(netcdf_file)
    
    try:
        # Open the NetCDF file
        ds = xr.open_dataset(netcdf_file)
        
        # Create the YAML specification
        yaml_spec = create_yaml_spec(ds, output_filename)
        
        # Write the YAML file
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_spec, f)
        
        print(f"[bold green]Created YAML specification:[/bold green] {yaml_file}")
        
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    finally:
        # Make sure to close the dataset
        if 'ds' in locals():
            ds.close()


def create_yaml_spec(ds, output_filename):
    """
    Create a YAML specification from an xarray Dataset.
    
    Parameters
    ----------
    ds : xr.Dataset
        The dataset to analyze
    output_filename : str
        The filename to use in the YAML spec
        
    Returns
    -------
    dict
        The YAML specification
    """
    # Create the top-level structure
    yaml_spec = {output_filename: {}}
    file_spec = yaml_spec[output_filename]
    
    # Add dimensions
    file_spec['dimensions'] = {}
    for dim_name, dim_size in ds.dims.items():
        # Check if this dimension has coordinate data
        if dim_name in ds.coords:
            coord_data = ds[dim_name].values
            
            # Determine if it's a datetime dimension
            if np.issubdtype(coord_data.dtype, np.datetime64):
                # Handle datetime dimension
                file_spec['dimensions'][dim_name] = {
                    'size': dim_size,
                    'dtype': 'datetime',
                    'start_date': str(coord_data[0])[:10],  # YYYY-MM-DD format
                    'freq': infer_time_frequency(coord_data)
                }
            else:
                # Handle numeric dimension
                try:
                    # Check if it's a regular sequence
                    if dim_size > 1:
                        step = (coord_data[-1] - coord_data[0]) / (dim_size - 1)
                        if np.allclose(np.diff(coord_data), step):
                            file_spec['dimensions'][dim_name] = {
                                'size': dim_size,
                                'start': float(coord_data[0]),
                                'step': float(step)
                            }
                        else:
                            # Irregular spacing, just use size
                            file_spec['dimensions'][dim_name] = dim_size
                    else:
                        # Only one element, just use size
                        file_spec['dimensions'][dim_name] = dim_size
                except (TypeError, ValueError, IndexError):
                    # Fallback to simple dimension
                    file_spec['dimensions'][dim_name] = dim_size
        else:
            # Simple dimension without coordinate data
            file_spec['dimensions'][dim_name] = dim_size
    
    # Add variables
    file_spec['variables'] = {}
    for var_name, var_data in ds.data_vars.items():
        var_spec = {}
        
        # Add dimensions
        var_spec['dimensions'] = list(var_data.dims)
        
        # Use simple normal distribution by default
        var_spec['distribution'] = 'normal'
        
        # Set basic parameters based on data range
        data = var_data.values
        valid_data = data[~np.isnan(data)] if hasattr(data, 'mask') or np.isnan(data).any() else data
        
        if len(valid_data) > 0:
            mean_val = float(np.mean(valid_data))
            std_val = float(np.std(valid_data)) if len(valid_data) > 1 else 1.0
            var_spec['params'] = {
                'mean': mean_val,
                'std': std_val
            }
        else:
            var_spec['params'] = {
                'mean': 0.0,
                'std': 1.0
            }
        
        # Add attributes
        if var_data.attrs:
            var_spec['attrs'] = dict(var_data.attrs)
        
        file_spec['variables'][var_name] = var_spec
    
    # Add global attributes
    if ds.attrs:
        file_spec['global_attrs'] = dict(ds.attrs)
        
        # Add creation date if not present
        if 'history' not in file_spec['global_attrs']:
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_spec['global_attrs']['history'] = f"Created on {current_date}"
    
    return yaml_spec


def infer_time_frequency(time_values):
    """
    Infer the frequency of a time series.
    
    Parameters
    ----------
    time_values : np.array
        Array of datetime64 values
        
    Returns
    -------
    str
        Pandas frequency string
    """
    if len(time_values) < 2:
        return 'D'  # Default to daily
    
    # Calculate the most common difference
    time_diffs = np.diff(time_values)
    
    # Convert to days for easier comparison
    time_diffs_days = time_diffs.astype('timedelta64[D]').astype(float)
    
    median_diff = np.median(time_diffs_days)
    
    # Determine frequency based on median difference
    if median_diff < 0.1:  # Less than 2.4 hours
        return 'H'  # Hourly
    elif median_diff < 2:  # Less than 2 days
        return 'D'  # Daily
    elif 6 <= median_diff <= 8:  # About a week
        return 'W'  # Weekly
    elif 28 <= median_diff <= 31:  # About a month
        return 'M'  # Monthly
    elif 90 <= median_diff <= 92:  # About a quarter
        return 'Q'  # Quarterly
    elif 365 <= median_diff <= 366:  # About a year
        return 'Y'  # Yearly
    else:
        return 'D'  # Default to daily


# Removed complex distribution inference function


if __name__ == "__main__":
    main()
