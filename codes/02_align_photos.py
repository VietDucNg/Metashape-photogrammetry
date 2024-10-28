# Viet Nguyen
# University of Greifswald
# based on the Geo-SfM course from The University Centre in Svalbard 
# and the work from Derek Young and Alex Mandel (https://github.com/open-forest-observatory/automate-metashape/tree/main).

import Metashape
import time

doc = Metashape.app.document # accesses the current project and document

def diff_time(t2, t1):
    '''
    Give a end and start time, subtract, and round
    '''
    total = str(round(t2-t1, 1))
    return total


def reset_region(doc):
    '''
    Reset the region and make it much larger than the points; necessary because if points go outside the region, they get clipped when saving
    '''

    doc.chunk.resetRegion()
    region_dims = doc.chunk.region.size
    region_dims[2] *= 3
    doc.chunk.region.size = region_dims

    return True

#### Align photos
# Match photos, align cameras, optimize cameras

# get a beginning time stamp
timer2a = time.time()

# Align cameras
doc.chunk.matchPhotos(downscale=2, # USGS (1) # medium(2) for vegetation as OFO
                      generic_preselection=True, 
                      reference_preselection=True,                 
                      reference_preselection_mode = Metashape.ReferencePreselectionSource,
                      filter_mask = True,
                      mask_tiepoints=False, 
                      filter_stationary_points=True, 
                      keypoint_limit=40000, # 60000 for high quality photos
                      keypoint_limit_per_mpx = 5000,  
                      tiepoint_limit=4000,
                      keep_keypoints=True, 
                      guided_matching=True, 
                      reset_matches=False)

doc.chunk.alignCameras(adaptive_fitting = True, # True as OFO
                       reset_alignment = False)

# reset the region
reset_region(doc)
print('Reset region finish.')

# save project
doc.save()

# get an ending time stamp
timer2b = time.time()

# calculate difference between end and start time to 1 decimal place
time2 = diff_time(timer2b, timer2a)

# print time record
print('Alignment finish after',time2,'second.')