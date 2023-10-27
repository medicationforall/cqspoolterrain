import cadquery as cq
from cqspoolterrain import pipe

ex_platform = pipe.platform()

#show_object(ex_platform)
cq.exporters.export(ex_platform,"stl/platform_pipe.stl")