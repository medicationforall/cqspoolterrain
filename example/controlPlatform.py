import cadquery as cq
from cqspoolterrain import ControlPlatform

bp_control = ControlPlatform()
bp_control.render_stripes = True
bp_control.render_floor = True
bp_control.make()
controlPlatform = bp_control.build()

cq.exporters.export(controlPlatform,"stl/controlPlatform.stl")