import cadquery as cq
from . import Base

class SpoolCladding(Base):
    def __init__(
            self,
            start_angle = 0,
            end_angle = 360,
            rotate_solid = True,
            count = 17,
            clad_width = 33,
            clad_height = 5,
            clad_inset = 5
        ):
        super().__init__()
        
        #arc parameters
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.rotate_solid = rotate_solid
        self.count = count
        
        #clad
        self.clad_height = clad_height
        self.clad_width = clad_width
        self.clad_inset = clad_inset
        
        # parts 
        self.cladding = None
        
    def _make_clad(self, loc):
        length = self.parent.height - self.parent.wall_width*2
        width = self.clad_width
        height = self.clad_height
        clad = (
            cq.Workplane("XY").box(length,width,height)
            .rotate((0,1,0),(0,0,0), 90)
            .translate((-1*(height/2)-self.clad_inset,0,0))
        )
        return clad.val().located(loc)
    
    def __make_cladding(self):
        cladding_arc =(
            cq.Workplane("XY")
            .polarArray(
                radius  = self.parent.radius, 
                startAngle  = self.start_angle, 
                angle  = self.end_angle, 
                count  = self.count,
                fill = True,
                rotate = self.rotate_solid
            )
            .eachpoint(callback = self._make_clad)
        )
        
        self.cladding = cladding_arc
        
    def make(self, parent = None):
        super().make(parent)
        self.__make_cladding()

        
        
    def build(self):
        super().build()
        return self.cladding