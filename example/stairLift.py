import cadquery as cq
from cqspoolterrain import StairLift

bp_stairs = StairLift()
bp_stairs.bp_stairs.render_hollow = False
bp_stairs.make()
stairs = bp_stairs.build()
#show_object(stairs)
cq.exporters.export(stairs,"stl/stair_Lift.stl")