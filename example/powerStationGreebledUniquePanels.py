import cadquery as cq
from cqspoolterrain import PowerStation, SpoolCladdingGreebledUnique

bp_power = PowerStation()
bp_power.bp_cladding = SpoolCladdingGreebledUnique()
bp_power.bp_cladding.seed="uniquePanels"
bp_power.make()
power = bp_power.build()
#show_object(power)
cq.exporters.export(power,f"stl/powerStation_seed_{bp_power.bp_cladding.seed}.stl")