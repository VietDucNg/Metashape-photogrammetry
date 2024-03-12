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
timer5a = time.time()

# build mesh
doc.chunk.buildModel(surface_type=Metashape.HeightField, 
                     interpolation=Metashape.EnabledInterpolation, 
                     face_count=Metashape.MediumFaceCount, # medium as OFO
                     source_data=Metashape.DenseCloudData, 
                     vertex_colors=True, 
                     vertex_confidence=True, 
                     subdivide_task=False)
                     
# decimate mesh to half of face count
doc.chunk.decimateModel(face_count = len(doc.chunk.model.faces) / 2)
# smooth mesh
doc.chunk.smoothModel(50)

doc.save()

# get an ending time stamp for the previous step
timer5b = time.time()

# calculate difference between end and start time to 1 decimal place
time5 = diff_time(timer5b, timer5a)
print('Build Mesh finished after',time5,'seconds.')
