import cadquery as cq
from cqspoolterrain import Spool, Cradle, Base, StairLift, ControlPlatform
from cqindustry import Walkway, Platform
from cadqueryhelper import shape

class PowerStation(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.p_spool = {}
        self.p_spool['height'] = 60
        self.p_spool['radius'] = 97.5
        self.p_spool['wall_width'] =4
        self.p_spool['cut_radius'] = 36.5
        
        self.p_cradle = {}
        self.p_cradle['height'] = self.p_spool['radius'] - self.p_spool['cut_radius']+2
        self.p_cradle['angle'] = 45
        
        self.p_stairs = {}
        
        self.p_control = {}
        self.p_control['render_stripes'] = True
        self.p_control['render_floor'] = True
        
        # not used
        self.p_walkway = {}
        
        # blueprints
        self.bp_spool = Spool(**self.p_spool)
        self.bp_cradle = Cradle(**self.p_cradle)
        self.bp_walk = Walkway()
        self.bp_stairs = StairLift(**self.p_stairs)
        self.bp_control = ControlPlatform(**self.p_control)
        
    def make(self, parent = None):
        super().make(parent)
        self.bp_spool.make(self)
        self.bp_cradle.make(self)
        self.bp_walk.make()
        self.bp_stairs.make(self)
        self.bp_control.make(self)
        
    def build(self):
        super().build()
        spool = (
            self.bp_spool.build()
            .rotate((1,0,0),(0,0,0),90)
            .translate((0,0,self.bp_spool.radius))
        )
        
        cradle = self.bp_cradle.build()
        walkway = self.bp_walk.build().rotate((0,0,1),(0,0,0), 90)
        stairs = self.bp_stairs.build()
        controlPlatform = self.bp_control.build()
        
        #----- Build the building
        walk_z_translate = (self.bp_walk.height /2)+self.bp_cradle.height +10
        building = (
            cq.Workplane("XY")
            .union(cradle.translate((0,0,self.bp_cradle.height/2)))
            .add(spool.translate((0,0,2)))
            .add(walkway.translate((0,0,walk_z_translate)))
            .add(stairs.translate((0,-75,self.bp_stairs.height/2)))
            .add(controlPlatform.translate((0,75,self.bp_control.height/2)))
        )
        
        #mini = cq.Workplane("XY").cylinder(32, 12.5).translate((0,-135,17))
        return building