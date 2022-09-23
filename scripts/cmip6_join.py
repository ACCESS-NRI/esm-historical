import xarray as xr
import os


def combine_files(var_path):
    fns = os.listdir(var_path)
    dates = [
        int(d)
        for fn in fns
        for d in fn.split('_')[-1].split('.')[0].split('-')
    ]

    out_fn = '_'.join(fns[0].split('_')[:-1]) + f"_{min(dates)}-{max(dates)}.nc"
    out_path = os.path.join(var_path, out_fn)
    ds = xr.open_mfdataset(os.path.join(var_path, '*'), combine='by_coords')

    ds.to_netcdf(out_path)
    for fn in fns:
        os.remove(os.path.join(var_path, fn))
    return 0


output_loc = os.environ.get('OUTPUT_LOC')
parent_variant_label = os.environ.get('parent_variant_label')
experiment_id = os.environ.get('experiment_id')
activity_id = os.environ.get('activity_id')

base_path = os.path.join(output_loc, activity_id, 'CSIRO', 'ACCESS-ESM1-5', experiment_id, parent_variant_label)

count = 0
for dirpath, dirnames, filenames in os.walk(base_path):
    if not dirnames:
        count +=1

print(count)
# for dir1 in os.listdir(base_path):
#     for dir2 in os.listdir(os.path.join(base_path, dir1)):
#         for dir3 in os.listdir(os.path.join(base_path, dir1, dir2)):
#             for dir4 in os.listdir(os.path.join(base_path, dir1, dir2, dir3)):
#                 var_path = os.path.join(base_path, dir1, dir2, dir3, dir4)
                
#                 print(var_path)
#                 combine_files(var_path)
#                 break
#             break
#         break
#     break



# fns = os.listdir(var_path)
# dates = [
#     int(d)
#     for fn in fns
#     for d in fn.split('_')[-1].split('.')[0].split('-')
# ]

# out_fn = '_'.join(fns[0].split('_')[:-1]) + f"_{min(dates)}-{max(dates)}.nc"
# out_path = os.path.join(var_path, out_fn)

