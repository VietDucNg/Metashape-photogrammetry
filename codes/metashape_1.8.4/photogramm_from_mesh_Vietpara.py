# Viet Nguyen
# University of Greifswald
# based on the Geo-SfM course from The University Centre in Svalbard 
# and the work from Derek Young and Alex Mandel (https://github.com/open-forest-observatory/automate-metashape/tree/main).

# project crs
EPSG = "EPSG::5650"

import Metashape 
from pathlib import Path
import time

doc = Metashape.app.document # accesses the current project and document
chunk = doc.chunk # access the active chunk

def diff_time(t2, t1):
    '''
    Give a end and start time, subtract, and round
    '''
    total = str(round(t2-t1, 1))
    return total

def reset_region(doc):
    '''
    Reset the region and make it much larger than the points; 
    necessary because if points go outside the region,
    they get clipped when saving
    '''
    doc.chunk.resetRegion()
    region_dims = doc.chunk.region.size
    region_dims[2] *= 3
    doc.chunk.region.size = region_dims
    return True

def progress_print(p):
        print('Current task progress: {:.2f}%'.format(p))


######################
#### rename photo ####
######################

for c in chunk.cameras: # loops over all cameras in the active chunk
    cp = Path(c.photo.path) # gets the path for each photo
    c.label = str(cp.parent.name) + '/' + cp.name # renames the camera label in the metashape project to include the parent directory of the photo


#####################
#### align photo ####
#####################

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
                      tiepoint_limit=10000,
                      keep_keypoints=True, 
                      guided_matching=True, 
                      reset_matches=False)

doc.chunk.alignCameras(adaptive_fitting = True, # True as OFO
                       reset_alignment = False)

# reset the region
reset_region(doc)
print('Reset region finish.')

# get an ending time stamp
timer2b = time.time()

# calculate difference between end and start time to 1 decimal place
time2 = diff_time(timer2b, timer2a)

# print time record
print('Alignment finish after',time2,'second.')


###############################################
#### optimize camera and filter tie points ####
###############################################

class metashape_tiepoint_filter:
    def __init__(self,ms_path: Path):

        if not ms_path == None:
            self.doc = Metashape.Document()
            self.doc.open(ms_path.as_posix())
        else:
            self.doc = Metashape.app.document
        self.chunk = self.doc.chunk
        self.total_tie_points = len(self.chunk.point_cloud.points)

    def standard_run(self):
        if len(self.chunk.dense_clouds) == 0:
            self.optimize_cameras()
            self.filter_reconstruction_uncertainty()
            self.optimize_cameras()
            # self.doc.save()
            self.filter_projection_accuracy()
            self.optimize_cameras()
            # self.doc.save()
            self.filter_reprojection_error()
            self.optimize_cameras()
            self.reset_region()
            self.set_label_naming_template()
            # self.doc.save()
        else:
            print("Dense cloud exists... Ignoring..")

    
    def reset_region(self):
    # Reset the region and make it much larger than the points; necessary because if points go outside the region, they get clipped when saving
        self.chunk.resetRegion()
        region_dims = self.chunk.region.size
        region_dims[2] *= 3
        self.chunk.region.size = region_dims
        print('Reset region finish.')


    def optimize_cameras(self, parameters = None):
        print("optimize_cameras")

        self.chunk.optimizeCameras(
            fit_corrections=True,
            tiepoint_covariance=True,
            adaptive_fitting = True,
            progress=progress_print
        )
        
    def filter_reconstruction_uncertainty(self, x = 15): # 10 according to USGS # 15 according to OFO
        print("filter_reconstruction_uncertainty")
        self.chunk = self.chunk.copy()
        f = Metashape.PointCloud.Filter()
        f.init(self.chunk, criterion = Metashape.PointCloud.Filter.ReconstructionUncertainty)
        while (len([i for i in f.values if i >= x])/self.total_tie_points) >= 0.2: # 0.5 according to usgs # 0.2 according to OFO
            x += 0.1
        x = round(x,1)
        self.chunk.label = f"RecUnc={x}"
        f.removePoints(x)
        
    def filter_projection_accuracy(self, x = 2): # 3 according to usgs # 2 according to OFO
        print("filter_projection_accuracy")
        # self.chunk = self.chunk.copy()
        f = Metashape.PointCloud.Filter()
        f.init(self.chunk, criterion = Metashape.PointCloud.Filter.ProjectionAccuracy)
        while (len([i for i in f.values if i >= x])/len(self.chunk.point_cloud.points)) >= 0.3: # 0.5 according to usgs # 0.3 according to OFO
            x += 0.1
        x = round(x,1)
        # old version with self.chunk.coppy(): self.chunk.label = f"{self.chunk.label.split('Copy of ')[1]}_ProjAcc={x}"
        self.chunk.label = f"{self.chunk.label}_ProjAcc={x}"
        f.removePoints(x)
        
    def filter_reprojection_error(self, x = 0.3):  # 0.3 according to OFO
        print("filter_reprojection_error")
        # self.chunk = self.chunk.copy()
        f = Metashape.PointCloud.Filter()
        f.init(self.chunk, criterion = Metashape.PointCloud.Filter.ReprojectionError)
        while (len([i for i in f.values if i >= x])/len(self.chunk.point_cloud.points)) >= 0.05:# 0.1 as usgs # 0.05 according to OFO
            x += 0.005
        print('Reprojection error level:',x)
        x = round(x,2)
        # old version with self.chunk.coppy(): self.chunk.label = f"{self.chunk.label.split('Copy of ')[1]}_RepErr={x}"
        self.chunk.label = f"{self.chunk.label}_RepErr={x}"
        f.removePoints(x)

    def set_label_naming_template(self):
        self.chunk.label = f"{self.chunk.label}"

a = metashape_tiepoint_filter(None)
a.standard_run()


###########################
#### build dense cloud ####
###########################

### Build depth maps

# get a beginning time stamp for the next step
timer4a = time.time()

# build depth maps only instead of also building the dense cloud ##?? what does
doc.chunk.buildDepthMaps(downscale = 2, # medium (4) according to OFO
                         filter_mode = Metashape.MildFiltering) # Moderate according to OFO


### Build dense cloud

# get a beginning time stamp for the next step
timer3a = time.time()

# build dense cloud
doc.chunk.buildDenseCloud(point_colors = True, 
                          point_confidence = True, 
                          max_neighbors=100)

# get an ending time stamp for the previous step
timer4b = time.time()

# calculate difference between end and start time to 1 decimal place
time4 = diff_time(timer4b, timer4a)
print('Build Dense cloud finished after',time4,'seconds.')


####################
#### build mesh ####
####################

# get a beginning time stamp for the next step
timer5a = time.time()

# build mesh
doc.chunk.buildModel(surface_type=Metashape.HeightField, 
                     interpolation=Metashape.EnabledInterpolation, 
                     face_count=Metashape.MediumFaceCount, # medium as OFO
                     source_data=Metashape.DenseCloudData, 
                     vertex_colors=True, 
                     vertex_confidence=True)
                     
# decimate mesh to half of face count
doc.chunk.decimateModel(face_count = len(doc.chunk.model.faces) / 2)
# smooth mesh
doc.chunk.smoothModel(50)

# get an ending time stamp for the previous step
timer5b = time.time()

# calculate difference between end and start time to 1 decimal place
time5 = diff_time(timer5b, timer5a)
print('Build Mesh finished after',time5,'seconds.')


###########################
#### build orthomosaic ####
###########################

# get a beginning time stamp for the next step
timer6a = time.time()

# prepping projection
projection = Metashape.OrthoProjection()
projection.crs = Metashape.CoordinateSystem(EPSG)

# build orthomosaic
doc.chunk.buildOrthomosaic(surface_data=Metashape.ModelData,
                           blending_mode=Metashape.MosaicBlending,
                           ghosting_filter=True,
                           fill_holes=True,
                           cull_faces=True,
                           refine_seamlines=True,   # True as OFO           
                           projection=projection)

# get an ending time stamp for the previous step
timer6b = time.time()

# calculate difference between end and start time to 1 decimal place
time6 = diff_time(timer6b, timer6a)
print('Build Orthomosaic finished after',time6,'seconds.') 


###################
#### build DEM ####
###################

# get a beginning time stamp for the next step
timer7a = time.time()

# prepping params for buildDem
projection = Metashape.OrthoProjection()
projection.crs = Metashape.CoordinateSystem(EPSG)

doc.chunk.buildDem(source_data = Metashape.DenseCloudData,
                interpolation = Metashape.EnabledInterpolation,
                projection = projection)

# get an ending time stamp for the previous step
timer7b = time.time()

# calculate difference between end and start time to 1 decimal place
time7 = diff_time(timer7b, timer7a)
print('Build DEM finished after',time7,'seconds.')

# save project
doc.save()