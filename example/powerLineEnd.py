import cadquery as cq
from cqspoolterrain import power_line_end

end_cap = power_line_end()


#show_object(end_cap)
cq.exporters.export(end_cap,"stl/powerLine_end.stl")