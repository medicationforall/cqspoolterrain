import cadquery as cq
from cqspoolterrain import pipe

pipe_line = pipe.straight(
    length = 75, 
    connector_length=2, 
    connector_radius = 11.5
)
#show_object(power_line)
cq.exporters.export(pipe_line,"stl/pipe_straight.stl")