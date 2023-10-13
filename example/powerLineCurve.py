import cadquery as cq
from cqspoolterrain import power_line_curve

curve_power_line, curve_power_line_2 =  power_line_curve()

cq.exporters.export(curve_power_line,"stl/powerLine_curve_left.stl")
cq.exporters.export(curve_power_line_2,"stl/powerLine_curve_right.stl")