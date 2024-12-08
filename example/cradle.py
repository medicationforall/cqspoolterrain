import cadquery as cq
from cqspoolterrain import Spool,Cradle

bp_spool = Spool()
bp_spool.make()
spool_ex = (
      bp_spool.build()
      .rotate((1,0,0),(0,0,0),90)
      .translate((0,0,bp_spool.radius))
)

bp = Cradle()
bp.height = bp_spool.radius - bp_spool.cut_radius+2
bp.angle = 45
bp.make(bp_spool)
cradle_ex = bp.build().translate((0,0,bp.height/2))

#show_object(cradle_ex)
cq.exporters.export(cradle_ex,"stl/cradle.stl")