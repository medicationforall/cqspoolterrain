import cadquery as cq
from cqspoolterrain import ControlPlatformPrint

bp_control = ControlPlatformPrint()
bp_control.length = 150
bp_control.width = 75
bp_control.height = 71

bp_control.y_height = 8
bp_control.frame_insert_margin = .8
bp_control.frame_insert_height = 1
bp_control.frame_insert_height_margin = 1

bp_p = bp_control.platform_bp
bp_p.height = 4
bp_p.corner_chamfer = 4

bp_p.render_floor = True
bp_p.render_stripes = True
bp_p.bar_width = 10
bp_p.stripe_width = 5
bp_p.stripe_padding = .3

bp_control.make()

control_platform = bp_control.build_print_patform()
#show_object(control_platform.translate((0,0,3)))
cq.exporters.export(control_platform,"stl/Platform.stl")


frame = bp_control.build_print_frame()
#show_object(frame)

frame_single = bp_control.build_print_frame_single()
#show_object(frame_single)
cq.exporters.export(frame_single,"stl/platformFrameSingle.stl")
