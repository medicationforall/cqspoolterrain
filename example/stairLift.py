import cadquery as cq
from cqspoolterrain import StairLift

bp_stairs = StairLift()
bp_stairs.make()
stairs = bp_stairs.build()
#show_object(stairs)
cq.exporters.export(stairs,"stl/stairLift.stl")