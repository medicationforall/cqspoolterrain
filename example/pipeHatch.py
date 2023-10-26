import cadquery as cq
from cqspoolterrain import pipe


con = pipe.connector(
    length=2, 
    radius=11.5, 
    face_height = 23
)

h_ex = pipe.hatch(con)

cq.exporters.export(h_ex,"stl/pipe_hatch.stl")
