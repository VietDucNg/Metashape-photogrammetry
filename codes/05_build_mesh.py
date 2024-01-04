import Metashape
import time

doc = Metashape.app.document # accesses the current project and document

def diff_time(t2, t1):
    '''
    Give a end and start time, subtract, and round
    '''
    total = str(round(t2-t1, 1))
    return total

### Build Mesh

# get a beginning time stamp for the next step
timer3a = time.time()

# build mesh
doc.chunk.buildModel(surface_type=Metashape.Arbitrary, 
                     interpolation=Metashape.EnabledInterpolation, face_count=Metashape.HighFaceCount, 
                     source_data=Metashape.DenseCloudData, 
                     vertex_colors=True, vertex_confidence=True, subdivide_task=False)
doc.save()

# get an ending time stamp for the previous step
timer3b = time.time()

# calculate difference between end and start time to 1 decimal place
time3 = diff_time(timer3b, timer3a)
print('Build Dense cloud finished after',time3,'seconds.')
