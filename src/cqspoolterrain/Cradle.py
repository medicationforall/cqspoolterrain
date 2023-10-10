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
        self.spool_padding = 2
        
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
        if self.parent:
            self.parent.make()
        self.__make_cradle()
        
    def build(self):
        super().build()
        if self.parent:
            cut_spool = (
                self.parent.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.parent.radius))
            )
            return (
                cq.Workplane("XY")
                .union(self.cradle.translate((0,0,self.height/2)))
                .cut(cut_spool.translate((0,0,self.spool_padding)))
            ).translate((0,0,-1*(self.height/2)))

        return self.cradle