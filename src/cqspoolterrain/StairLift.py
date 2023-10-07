import cadquery as cq
from . import Base

class StairLift(Base):
    def __init__(
            self,
            length = 150,
            width = 75,
            height = 75,
            stair_count = 9
        ):
        super().__init__()
        # parameters
        self.length = length
        self.width = width
        self.height = height
        
        self.stair_count = stair_count
        
        #parts
        self.stairs = None
        
    def __make_step(self, i, stair_interval):
        step = cq.Workplane("XY").box(
            stair_interval,
            self.width/2, 
            stair_interval*(i+1)
        )
        
        cut_out = cq.Workplane("XY").box(
            stair_interval,
            (self.width/2)-4, 
            stair_interval-2
        ).faces("Z").edges("X").chamfer(2)
        
        #return cut_out
        cut_z_translate = ((stair_interval/2)*(i))-1
        return step.cut(cut_out.translate((0,0,cut_z_translate)))
        
    def __make_stairs(self):
        stair_length = self.length/2
        stair_interval = stair_length / self.stair_count
        
        stairs =(
            cq.Workplane("XY")
        )
        
        for i in range(self.stair_count):
            step = self.__make_step(i, stair_interval)
            stairs = stairs.union(
                step.translate((
                    stair_length-(stair_interval/2)-stair_interval*i,
                    -1*(self.width/4),
                    -1*(self.height/2)+(stair_interval*(i+1)/2)
                )))
            
        self.stairs = stairs
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_stairs()
        
    
    def build(self):
        super().build()
        walkway = cq.Workplane("XY").box(self.length,self.width/2,self.height)
        overlook = cq.Workplane("XY").box(self.length/2,self.width/2,self.height)
        scene = (
            cq.Workplane("XY")
            .union(walkway.translate((0,self.width/4,0)))
            .union(overlook.translate((-self.length/4,-self.width/4,0)))
            .union(self.stairs)
        )
        return scene