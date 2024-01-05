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


### Build depth maps

# get a beginning time stamp for the next step
timer4a = time.time()

# build depth maps only instead of also building the dense cloud ##?? what does
doc.chunk.buildDepthMaps(downscale=1, filter_mode=Metashape.MildFiltering, reuse_depth = False, subdivide_task = False)
doc.save()


### Build dense cloud

# get a beginning time stamp for the next step
timer3a = time.time()

# build dense cloud
doc.chunk.buildDenseCloud(point_colors = True, point_confidence = True, keep_depth = True, subdivide_task = False)
doc.save()

# get an ending time stamp for the previous step
timer4b = time.time()

# calculate difference between end and start time to 1 decimal place
time4 = diff_time(timer4b, timer4a)
print('Build Dense cloud finished after',time4,'seconds.')
