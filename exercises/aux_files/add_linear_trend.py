import xarray as xr


def add_linear_trend(data, rule):
    numbers = rule.aux["numbers"]
    numbers = [int(n) for n in numbers.split()]
    # Convert the numbers into an xarray with timestamps:
    numbers = xr.DataArray(data=numbers, coords=[data.time])
    data += numbers
    return data
