#!/usr/bin/env python3
"""
Creates fake data files from yaml specification

Usage
-----
Make sure you are in the same environment as you have for ``pymor``! Then, you
can run:

    $ python create-fake-data.py data-skeletons.yaml
"""
import ruamel.yaml as yaml
import xarray as xr
from rich import print


def main():
    print("Generating fake data files!")


if __name__ == "__main__":
    main()
