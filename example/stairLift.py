import cadquery as cq
from cqspoolterrain import StairLift

bp_stairs = StairLift()
bp_stairs.make()
stairs = bp_stairs.build()

cq.exporters.export(stairs,"stl/stairLift.stl")