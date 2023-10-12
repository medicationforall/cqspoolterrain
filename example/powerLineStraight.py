import cadquery as cq
from cqspoolterrain import power_line_straight

power_line = power_line_straight(
    length = 75, 
    connector_length=2, 
    connector_radius = 11.5
)
#show_object(power_line)
cq.exporters.export(power_line,"stl/powerLine_straight.stl")