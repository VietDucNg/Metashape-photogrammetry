# Viet Nguyen
# University of Greifswald
# based on the Geo-SfM course from The University Centre in Svalbard 
# and the work from Derek Young and Alex Mandel (https://github.com/open-forest-observatory/automate-metashape/tree/main).

import Metashape
from pathlib import Path

def progress_print(p):
        print('Current task progress: {:.2f}%'.format(p))

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
            self.doc.save()
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
        
    def filter_reprojection_error(self, x = 0.3): # 0.3 according to OFO
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


