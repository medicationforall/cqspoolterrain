import cadquery as cq
from cqspoolterrain import PowerStation

bp_power = PowerStation()
bp_power.make()
power = bp_power.build()
#show_object(power)
cq.exporters.export(power,"stl/powerStation.stl")