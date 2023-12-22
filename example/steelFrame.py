import cadquery as cq
from cqspoolterrain import SteelFrame
    
bp_frame = SteelFrame()
bp_frame.make()
ex_frame = bp_frame.build()

#show_object(ex_frame)
cq.exporters.export(ex_frame,"stl/steelFrame.stl")