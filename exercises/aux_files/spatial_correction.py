def add_spatial_correction(data, rule):
    correction = rule.aux["spatial-correction"]
    # Rename to the same name as data:
    correction = correction.rename(random="tsurf")
    print(correction)
    print(80 * "-")
    print(data)
    print(80 * "=")
    return data + correction
