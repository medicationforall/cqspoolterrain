import cadquery as cq
from . import pipe_face

def connector(length=2, radius=11.5, face_height = 23):
    outline = (
        pipe_face()
        .extrude(length)
        .translate((0,0,-1))
        .rotate((0,1,0),(0,0,0),90)
        .translate((0,0,face_height/2))
    )

    connector_plate = (
        cq.Workplane("XY")
        .cylinder(length, radius)
        .rotate((0,1,0),(0,0,0),90)
        .translate((0,0,radius+.5))
    )
    
    combined = (
        connector_plate
        .union(outline)
        .translate((0,0,-1*(radius+.5)))
    )
    return combined