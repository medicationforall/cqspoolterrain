import cadquery as cq
from cqspoolterrain import Spool,Cradle


bp_spool = Spool()
#bp.height = 100
#bp.radius = 100
#bp.wall_width = 3
#bp.cut_radius = 40
#bp.internal_wall_width = 4
#bp.internal_z_translate = -3
bp_spool.make()
spool_ex = (
      bp_spool.build()
      .rotate((1,0,0),(0,0,0),90)
      .translate((0,0,bp_spool.radius))
)

bp = Cradle()
bp.height = bp_spool.radius - bp_spool.cut_radius+2
bp.angle = 45
bp.make()
cradle_ex = bp.build().translate((0,0,bp.height/2))

scene = (
    cq.Workplane("XY")
    .union(cradle_ex)
    .cut(spool_ex.translate((0,0,2)))
)

#show_object(scene)
cq.exporters.export(scene,"stl/cradle.stl")