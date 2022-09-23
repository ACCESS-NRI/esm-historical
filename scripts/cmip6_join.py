import xarray as xr
import os
import time


def combine_files(var_path):
    """
    Merges all netcdf files in a given directory, deleting the original files. 
    This assumes a CMIP6 naming convention with a suffice "_{START_DATE}_{END_DATE}.nc"
    """

    fns = os.listdir(var_path)

    # extract the start and end dates
    dates = [
        int(d)
        for fn in fns
        for d in fn.split('_')[-1].split('.')[0].split('-')
    ]

    # create output filepath in correct CMIP6 format with the new dates
    out_fn = '_'.join(fns[0].split('_')[:-1]) + f"_{min(dates)}-{max(dates)}.nc"
    out_path = os.path.join(var_path, out_fn)
    
    # open multi file dataset and save it
    ds = xr.open_mfdataset(os.path.join(var_path, '*'), combine='by_coords')
    ds.to_netcdf(out_path)

    # delete original files
    for fn in fns:
        os.remove(os.path.join(var_path, fn))
    return 0


# extract environment variables to determine APP4 output locations
output_loc = os.environ.get('OUTPUT_LOC')
parent_variant_label = os.environ.get('parent_variant_label')
experiment_id = os.environ.get('experiment_id')
activity_id = os.environ.get('activity_id')

# hard code CSIRO (is this the only option?) and ACCESS-ESM1-5 directories
base_path = os.path.join(output_loc, activity_id, 'CSIRO', 'ACCESS-ESM1-5', experiment_id, parent_variant_label)

# walk through directory, assuming bottom directories (those with no subdirectories) correspond to variables
# maybe this could be done via the APP4 database?
for var_path, dirnames, _ in os.walk(base_path):
    if not dirnames:

        print("Merging" var_path)
        t0 = time.time()

        combine_files(var_path)

        print(f"Took {time.time() - t0}s.")
        break
