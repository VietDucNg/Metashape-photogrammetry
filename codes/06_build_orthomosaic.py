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

### Build orthomosaic

# get a beginning time stamp for the next step
timer6a = time.time()

# prepping projection
projection = Metashape.OrthoProjection()
projection.crs = Metashape.CoordinateSystem("EPSG::4326")

# build orthomosaic
doc.chunk.buildOrthomosaic(surface_data=Metashape.ModelData,
                           blending_mode=Metashape.MosaicBlending,
                           ghosting_filter=False,
                           fill_holes=True,
                           cull_faces=False,
                           refine_seamlines=False,   # True as OFO           
                           subdivide_task=False,
                           projection=projection)
doc.save()

# get an ending time stamp for the previous step
timer6b = time.time()

# calculate difference between end and start time to 1 decimal place
time6 = diff_time(timer6b, timer6a)
print('Build Orthomosaic finished after',time6,'seconds.') 