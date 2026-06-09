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

### Build DEM

# get a beginning time stamp for the next step
timer7a = time.time()


# prepping params for buildDem
projection = Metashape.OrthoProjection()
projection.crs = Metashape.CoordinateSystem("EPSG::5650")

doc.chunk.buildDem(source_data = Metashape.DenseCloudData,
                interpolation = Metashape.EnabledInterpolation,
                projection = projection)
doc.save()

# get an ending time stamp for the previous step
timer7b = time.time()

# calculate difference between end and start time to 1 decimal place
time7 = diff_time(timer7b, timer7a)
print('Build DEM finished after',time7,'seconds.')