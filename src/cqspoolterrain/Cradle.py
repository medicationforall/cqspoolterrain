import cadquery as cq
from . import Base, power_line_straight

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
        
        self.cut_side_width = 3
        self.cut_side_padding = 3
        
        #shapes
        self.cradle = None
        self.cut_side = None
        self.power_line = None
        
    def __make_cradle(self):
        cradle = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.length,self.height,self.angle)
            .finalize()
            .extrude(self.width)
            .translate((0,0,-1*(self.width/2)))
            .rotate((1,0,0),(0,0,0),-90)
        )
        
        self.cradle = cradle
        
    def __make_cut_side(self):
        cut_side = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.length-self.cut_side_padding*5,self.height - self.cut_side_padding*2,self.angle)
            .finalize()
            .extrude(self.cut_side_width)
            .translate((0,0,-1*(self.cut_side_width/2)))
            .rotate((1,0,0),(0,0,0),-90)
        )
        self.cut_side = cut_side
        
    def __make_power_line(self):
        power_line =(
            power_line_straight(self.width)
            .rotate((0,0,1),(0,0,0),90)
        )
        self.power_line = power_line
        
        
    def make(self, parent=None):
        super().make(parent)
        print('cradle make')
        if self.parent:
            self.parent.make()
        self.__make_cradle()
        self.__make_cut_side()
        self.__make_power_line()
        
    def build(self):
        super().build()
        #log(self.cut_side)
        cut_y_translate = self.width/2 - self.cut_side_width/2
        scene = (
            cq.Workplane("XY")#.box(10,10,10)
            .union(self.cradle.translate((0,0,self.height/2))) 
            .cut(self.cut_side.translate((0,cut_y_translate,self.height/2)))
            .cut(self.cut_side.translate((0,-1*(cut_y_translate),self.height/2)))
        )
        
        scene = (
            scene
            .union(self.power_line.translate((self.length/4,0,0)))
            .union(self.power_line.translate((-1*(self.length/4),0,0)))
        )
        if self.parent:
            cut_spool = (
                self.parent.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.parent.radius))
            )
            scene = scene.cut(cut_spool.translate((0,0,self.spool_padding)))

       # return self.cut_side
        return scene.translate((0,0,-1*(self.height/2)))