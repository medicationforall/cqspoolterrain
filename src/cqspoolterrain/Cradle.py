import cadquery as cq
from . import Base

class Cradle(Base):
    def __init__(
            self, 
            length = 150,
            width = 75,
            height = 60,
            angle = 45
        ):
        super().__init__()
        #parameters
        self.length = length
        self.width = width
        self.height = height
        self.angle = angle
        
        #shapes
        self.cradle = None
        
    def __make_cradle(self):
        self.cradle = (
            cq.Workplane("XY")
            .box(self.length,self.width,self.height)
        )
        
        result2 = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.length,self.height,self.angle)
            .finalize()
            .extrude(self.width)
            .translate((0,0,-1*(self.width/2)))
            .rotate((1,0,0),(0,0,0),-90)
        )
        
        self.cradle = result2
        
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_cradle()
        
    def build(self):
        super().build()
        return self.cradle