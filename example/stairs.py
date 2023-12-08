import cadquery as cq
from cqspoolterrain import Stairs

bp = Stairs()
bp.length = 75
bp.width = 75
bp.height = 50
bp.stair_count = 5
bp.stair_chamfer = .5
bp.render_step_cut = True
bp.cut_padding = 10
bp.make()
ex_stairs = bp.build()

#show_object(stairs)
cq.exporters.export(ex_stairs,"stl/stairs.stl")