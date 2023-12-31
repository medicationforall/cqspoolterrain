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
from cadqueryhelper import Base

class Stairs(Base):
    def __init__(
            self,
            length = 75,
            width = 75,
            height = 75,
            stair_count = 9,
            stair_chamfer = None,
            render_step_cut = True,
            cut_padding = 4
        ):
        super().__init__()
        # parameters
        self.length = length
        self.width = width
        self.height = height

        self.stair_count = stair_count
        self.stair_chamfer = stair_chamfer
        
        self.render_step_cut = render_step_cut
        self.cut_padding = cut_padding

        #parts
        self.stairs = None

    def __make_step(self, i, stair_interval_lengh, stair_interval_height):
        step = cq.Workplane("XY").box(
            stair_interval_lengh,
            self.width, 
            stair_interval_height*(i+1)
        )
        
        if self.render_step_cut:
            cut_out = cq.Workplane("XY").box(
                stair_interval_lengh,
                (self.width)-self.cut_padding, 
                stair_interval_height-2
            ).faces("Z").edges("X").chamfer(2)
            
            #return cut_out
            cut_z_translate = ((stair_interval_height/2)*(i))-1
            return step.cut(cut_out.translate((0,0,cut_z_translate)))
        else:
            return step

    def __make_stairs(self):
        stair_length = self.length
        stair_interval_length = stair_length / self.stair_count
        stair_interval_height = self.height / self.stair_count
        
        stairs =(
            cq.Workplane("XY")
        )
        
        for i in range(self.stair_count):
            step = self.__make_step(
                i, 
                stair_interval_length,
                stair_interval_height
            )
            
            if self.stair_chamfer:
                step = step.faces("<Y").edges("Z").chamfer(self.stair_chamfer)
                
            stairs = stairs.union(
                step.translate((
                    stair_length-(stair_interval_length/2)-stair_interval_length*i,
                    0,
                    -1*(self.height/2)+(stair_interval_height*(i+1)/2)
                )))
            
        self.stairs = stairs.translate((-1*(stair_length/2),0,0))

    def make(self, parent=None):
        super().make(parent)
        self.__make_stairs()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.stairs)
        )
        return scene