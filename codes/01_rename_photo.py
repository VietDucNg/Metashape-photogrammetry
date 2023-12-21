import Metashape 
from pathlib import Path

doc = Metashape.app.document # accesses the current project and document
chunk = doc.chunk # access the active chunk

for c in chunk.cameras: # loops over all cameras in the active chunk
    cp = Path(c.photo.path) # gets the path for each photo
    c.label = str(cp.parent.name) + '/' + cp.name # renames the camera label in the metashape project to include the parent directory of the photo