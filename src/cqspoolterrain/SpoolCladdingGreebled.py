import cadquery as cq
import math
from . import SpoolCladding
from cadqueryhelper import irregular_grid

class SpoolCladdingGreebled(SpoolCladding):
    def __init__(self):
        super().__init__()
        self.seed = "test4"
    
    def __make_greebled_panel(self, length, width , height):    
        i_grid = irregular_grid(
            length = length,
            width = width,
            height = math.floor(height/2),
            max_height = height+1,
            col_size = 4,
            row_size = 3,
            align_z = True,
            include_outline = False,
            passes_count = 1000,
            seed = self.seed,
            make_item = None,
            union_grid = False,
        )
        return i_grid.translate((0,0,-1*(height/2)))
    
    def _make_clad(self, loc):
        length = self.parent.height - self.parent.wall_width*2
        width = self.clad_width
        height = self.clad_height
        
        greebled_panel = self.__make_greebled_panel(length,width,height)
        
        clad = (
            cq.Workplane("XY")
            .union(greebled_panel)
            .rotate((0,1,0),(0,0,0), -90)
            .translate((-1*(height/2)-self.clad_inset,0,0))
        )
        
        return clad.val().located(loc)