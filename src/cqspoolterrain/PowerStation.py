# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from . import Spool, Cradle, Base, StairLift, ControlPlatform, SpoolCladding 
from cqindustry import Walkway
from cqterrain import Ladder

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
        self.ladder_raise = 25
        self.ladder_increase = 10
        self.render_stairs = True
        self.render_control = True
        self.render_spool = True
        self.render_walkway = True
        self.render_cradle = True
        self.render_cladding = True
        self.render_ladder = True

        #self.p_cladding = {}
        
        # blueprints
        self.bp_spool = Spool(**self.p_spool)
        self.bp_cradle = Cradle(**self.p_cradle)
        self.bp_walk = Walkway()

        self.bp_stairs = StairLift(**self.p_stairs)
        self.bp_control = ControlPlatform(**self.p_control)
        self.bp_cladding = SpoolCladding()#(**self.p_cladding)
        self.bp_ladder = Ladder()
        self.bp_ladder.height=self.bp_spool.radius + self.ladder_increase
        
    def make(self, parent = None):
        super().make(parent)
        if self.render_spool: 
            self.bp_spool.make(self)

        if self.render_cradle:
            self.bp_cradle.make(self.bp_spool)

        if self.render_cladding:
            self.bp_cladding.make(self.bp_spool)

        if self.render_ladder:
            self.bp_ladder.make()

        if self.render_stairs:
            self.bp_stairs.make(self)

        if self.render_control:
            self.bp_control.make(self)

        if self.render_walkway:
            self.bp_walk.make()

        
    def build(self):
        super().build()
        building = cq.Workplane("XY")

        if self.render_spool:
            spool = (
                self.bp_spool.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(spool.translate((0,0,2)))
        
        if self.render_cladding:
            cladding = (
                self.bp_cladding.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(cladding.translate((0,0,2)))
            
        if self.render_ladder:
            ladder = self.bp_ladder.build()
            ladder_x_translate = self.bp_spool.cut_radius + self.bp_ladder.length/2
            ladder_y_translate = self.bp_spool.height/2 + self.bp_ladder.width/2
            ladder_z_translate = self.bp_spool.radius+1 + self.ladder_raise
            building = building.add(ladder.translate((ladder_x_translate,ladder_y_translate,ladder_z_translate)))
            building = building.add(ladder.translate((-ladder_x_translate,-ladder_y_translate,ladder_z_translate)))

        if self.render_cradle:
            cradle = self.bp_cradle.build()
            building = building.union(cradle.translate((0,0,self.bp_cradle.height/2)))
            
        if self.render_stairs:
            stairs = self.bp_stairs.build()
            building = building.add(stairs.translate((0,-75,self.bp_stairs.height/2)))

        if self.render_control:
            controlPlatform = self.bp_control.build()
            building = building.add(controlPlatform.translate((0,75,self.bp_control.height/2)))

        if self.render_walkway:
            walk_z_translate = (self.bp_walk.height /2)+self.bp_cradle.height +10
            walkway = self.bp_walk.build().rotate((0,0,1),(0,0,0), 90)
            building = building.add(walkway.translate((0,0,walk_z_translate)))
        
        return building
    
    def build_cladding(self):
        building = cq.Workplane("XY")
        if self.render_cladding:
            cladding = (
                self.bp_cladding.build()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.bp_spool.radius))
            )
            building = building.add(cladding.translate((0,0,2)))

        if self.render_cradle:
            cradle = self.bp_cradle.build()
            building = building.cut(cradle.translate((0,0,self.bp_cradle.height/2)))

        return building