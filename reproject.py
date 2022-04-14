import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

base_dir= '/home/deep/Documents/PaperFiles/'
reproject_data_dir = base_dir + 'Reproject_Data/'

def reproject_data(source_file, destination_file, template_file):
    with rasterio.open(template_file) as rc:
        dst_crs = rc.crs
        print(dst_crs)
    
        with rasterio.open(source_file) as src:
            transform, width, height = calculate_default_transform(
                rc.crs, rc.crs, rc.width, rc.height, *rc.bounds)
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': dst_crs,
                'transform': transform,
                'width': width,
                'height': height
            })
    
            with rasterio.open(destination_file, 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=src.crs,
                        resampling=Resampling.nearest)
        return destination_file
