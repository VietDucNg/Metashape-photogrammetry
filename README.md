![Metashape icon](/images/01_Metashape_logo.png)

# Metashape-photogrammetry

 *[Metashape](https://www.agisoft.com/)* step-by-step tutorial for photogrammetry (DEM, point clouds, orthomosaic, mesh, and texture) from arial images.

The tutorial prepared by Viet Nguyen (*[Earth Observation and Geoinformation Science Lab](https://geo.uni-greifswald.de/en/chairs/geographie/translate-to-english-fernerkundung-und-geoinformationsverarbeitung/)* - *[University of Greifswald](https://www.uni-greifswald.de/en/)*) based on  the *[Geo-SfM](https://unisvalbard.github.io/Geo-SfM/landing-page.html#)* course from *[The University Centre in Svalbard](https://www.unis.no/)*.

![uav photogrammetry image](/images/02_uav_photogrammetry.jpg)*<sup><sub>(https://www.inrae.fr/en/news/remote-sensing-dossier)</sub></sup>*


## Project structure
It is recommended to use the standardised project structure (or something similar) throughout all future projects. 

    {project_directory} (The folder with all files related to this project)
    |   overview_img.{ext}
    |   description.txt
    ├───config (where you place your configuration files)
            {cfg_0001}.yml
            {cfg_0002}.yml
            ...
    ├───data (where you unzipped the files to)
    ├───────f0001 (The folder with images acquired on the first flight)
    |           {img_0001}.{ext}
    |           {img_0002}.{ext}
    |           ...
    ├───────f0002 (The folder with images acquired on the second flight)
    |           {img_0001}.{ext}
    |           {img_0002}.{ext}
    |           ...
    |       ...
    ├───────f9999 (The folder with images acquired on the last flight)
    |           {img_0001}.{ext}
    |           {img_0002}.{ext}
    |           ...
    ├───────gcps
    |           (...)
    ├───────GNSS
    |           (...)
    ├───export (where you place export models and files)
            ...
    └───metashape (This is where you save your Agisoft Metashape projects to)
            {metashape_project_name}.psx
            .{metashape_project_name}.files
            {metashape_project_name}_processing_report.pdf
            (optionally: {metashape_project_name}.log)


The standardised project structures are important for automated processing and archiving.

## Getting started
### 1. Add photos
It is helpful to include the subfolder name in the photo file name in Metashape (to differentiate photos from which flight). Below is the [code](/codes/01_rename_photo.py) for Python console to rename all photos to reflect the subfolder they are in.

```python
import Metashape 
from pathlib import Path

doc = Metashape.app.document # accesses the current project and document
chunk = doc.chunk # access the active chunk

for c in chunk.cameras: # loops over all cameras in the active chunk
    cp = Path(c.photo.path) # gets the path for each photo
    c.label = str(cp.parent.name) + '/' + cp.name # renames the camera label in the metashape project to include the parent directory of the photo
```

### 2. Estimate image quality
 This is done by right clicking any of the *photos* in a *Chunk*, then selecting *Estimate Image Quality…*, and select all photos to be analysed, as shown in figure below.

 ![estimate image quality](/images/03_estimate_image_quality.gif)

 Open the *Photos* pane by clicking *Photos* in the View menu. Then, make sure to view the details rather than icons to check the Quality for each image. 
 
 
 > [!TIP]  
 > Then, filter on quality and Disable all selected cameras that do not meet the standard. Agisoft recommends a Quality of at least 0.5.

 ### 3. Align photos
 ![align photo](/images/04_align_photo.png)

 #### 3.1. Improve alignment

The following optimizations to improve quality of the sparse point cloud including *[Optimize Camera Alignment](#optimize-camera-alignment)*, *[Filter uncertain points](#filtering-uncertain-points)*, *[Filter by Projection accuracy](#filter-by-projection-accuracy)*, *[Filtering by Reprojection Error](#filtering-by-reprojection-error)*. Those optimizations can be automated by Python console using this [code](/codes/02_filter_tie_point).

 > [!NOTE]
 > Save project and backup data before any destructive actions

 ##### Optimize Camera Alignment
 This is done by selecting *Optimize Cameras* from the *Tools* menu

 ![optimize camera](/images/05_optimize_camera.png)

 Change the model view to show the Point Cloud Variance. Lower values (=blue) are generally better and more constrained.


##### Filter uncertain points
![filter uncertain points](/images/06_filter_by_reconstruction_uncertainty.gif)

A good value to use for uncertainty lever is 10, though make sure do not remove all points by doing so!. A rule of thumb is to select no more than two-thirds to half of all points, and then delete these by pressing the Delete key on the keyboard.

> [!TIP]
> After filtering points, it is important to once more optimize the alignment of the points. Doing so by revisiting the [Optimize Camera Alignment](#optimize-camera-alignment)

##### Filter by Projection accuracy
This time, select the points based on their *Projection accuracy*, aiming for a final Projection accuracy of 3.

![filter by projection accuracy](/images/07_filter_by_projection_accuracy.png)

> [!TIP]
> After filtering points, it is important to once more optimize the alignment of the points. Doing so by revisiting the [Optimize Camera Alignment](#optimize-camera-alignment)

##### Filter by Reprojection Error
A good value to use here is 0.3, though make sure you do not remove all points by doing so! As a rule of thumb, this final selection of points should leave you with approx. 10% of the points you started off with.

![filter by reprojection error](/images/08_filter_by_reprojection_error.png)

> [!TIP]
> After filtering points, it is important to once more optimize the alignment of the points. Doing so by revisiting the [Optimize Camera Alignment](#optimize-camera-alignment)

### 4. Dense point cloud

Select *Build Point Cloud* from the *Workflow* menu.

![dense point cloud](/images/09_dense_point_cloud.png)

Visualise the point confidence by clicking the gray triangle next to the nine-dotted icon and selecting *Point Cloud confidence*. The color coding (red = bad, blue = good).

#### 4.1. Filter by point confidence
Open *Tools/Point Cloud* in the menu and click on *Filter by confidence…* The dialog that pops up allows you to set minimal and maximal confidences. For example, try setting Min:50 and Max:255. After looking at the difference, reset the filter by clicking on *Reset filter* within the *Tools/Point Cloud* menu.

### 5. Mesh model

![mesh example](/images/14_mesh_animation.gif)

Selecting *Build Mesh* from the *Workflow* menu, you will be able to chose either Dense cloud or Depth map as the source. 

> [!TIP]  
> Depth maps may lead to better results when dealing with a big number of minor details. If you decide to use depth maps as the source data, then make sure to enable *Reuse depth maps* to save computational time!

![Mesh](/images/10_Mesh.png)

#### 5.1. Filter the mesh
Sometimes your mesh has some tiny parts that are not connected to the main model. These can be removed by the *Connected component filter*.

![filter mesh](/images/11_filter_mesh.gif)

### 6. Texture
Open *Build Texture* from the *Workflow* menu.

![build texture](/images/12_build_texture.png)

*Texture size/count* determines the quality of the texture. Anything over 16384 can lead to very large file sizes on your harddisk. On the other hand, anything less than 4096 is probably insufficient. For greatest compatibility, keep the *Texture size* at 4096, but increase the *count* to e.g. 5 or 10.

### 7. DEM
Select *Build DEM* from the *Workflow* menu.

It is recommended to use *Point Cloud* as the source data since it provides more accurate results and faster processing.

it ist recommended to keep the interpolation parameter **Disabled** for accurate reconstruction results since only areas corresponding to point cloud or polygonal points are reconstructed. Usually, this method is recommended for Mesh and Tiled Model data source.

### 8. Orthomosaic
Select *Build Orthomosaic* from the *Workflow* menu. To begin, you have to select the Projection parameter.
- Geographic projectionis often used for aerial photogrammetric surveys.

- Planar projection is helpful when working with models that have vertical surfaces, such as vertical digital outcrop models.

- Cylindrical projection can help reduce distortions when projecting cylindrical objects like tubes, rounded towers, or tunnels.

It is recommended to use *Mesh* as surface. For complete coverage, enable the *hole filling* option under *Blending mode* to fill in any empty areas of the mosaic.

![orthomosaic](/images/13_build_orthomosaic.png)

## Documenting
Open *File/Export* and select *Generate Report…* Store the report in the *metashape* folder with the project file.

