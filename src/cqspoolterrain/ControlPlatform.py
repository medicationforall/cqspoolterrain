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
from . import Base
from cqindustry import Platform
from cadqueryhelper import shape

class ControlPlatform(Base):
    def __init__(
            self,
            length = 150,
            width = 75,
            height = 70,
            platform_height = 5,
            render_floor = True,
            render_stripes = True,
            base_length = 75
        ):
        super().__init__()
        self.length = length
        self.width = width
        self.height = height
        
        # platform
        self.platform_height = platform_height
        self.render_floor = render_floor
        self.render_stripes = render_stripes
        
        # base
        self.base_length = base_length
        
        self.platform_bp = None
        self.platform = None
        self.frame = None
        self.corner_joins = None
        
    def __make_platform(self):
        self.platform_bp = Platform()
        self.platform_bp.width = self.width
        self.platform_bp.height = self.platform_height
        self.platform_bp.render_center_cut = False
        self.platform_bp.render_ladders = False
        self.platform_bp.render_floor = self.render_floor
        self.platform_bp.render_stripes = self.render_stripes
        self.platform_bp.corner_chamfer = 4
        self.platform_bp.make()
        
    def __make_frame(self):
        z_beam = shape.i_beam(
          length=self.height,
          width=5,
          height=10,
          web_thickness=2,
          flange_thickness=2,
          join_distance=1.3
        ).rotate((0,1,0),(0,0,0),90)
        
        y_beam = shape.i_beam(
          length=self.width-(10/2),
          width=5,
          height=10,
          web_thickness=2,
          flange_thickness=2,
          join_distance=1.3
        ).rotate((0,0,1),(0,0,0),90)
        
        c_x = (self.length/2)-(10/2)
        c_y = (self.width/2)-(5/2)
        frame = (
            cq.Workplane("XY")
            .add(z_beam.translate((c_x,c_y,0)))
            .add(z_beam.translate((-c_x,c_y,0)))
            .add(z_beam.translate((c_x,-c_y,0)))
            .add(z_beam.translate((-c_x,-c_y,0)))
            
            .add(z_beam.translate((0,-c_y,0)))
            .add(z_beam.translate((0,c_y,0)))
            
            .add(y_beam.translate((c_x,0,self.height/2)))
            .add(y_beam.translate((0,0,self.height/2)))
            .add(y_beam.translate((-c_x,0,self.height/2)))
        )
        
        self.frame = frame
        
    def __make_corner_joins(self):
        x_translate = self.width/2 - 5 - 5/2 +1.5
        z_translate = self.height/2 - 10/2 - 5/2
        corner_join = (
            shape.corner_join(5,5,5,1,1)
            .rotate((0,1,0),(0,0,0),90)
        )
        
        frame_joins = (
            cq.Workplane("XY")
            .union(corner_join.translate((0,x_translate,z_translate)))
            .union(corner_join.rotate((0,0,1),(0,0,0),180).translate((0,-x_translate,z_translate)))
        )
        frame_x_translate = self.length/2  - 10/2
        joins = (
            cq.Workplane("XY")
            .union(frame_joins)
            .union(frame_joins.translate((frame_x_translate,0,0)))
            .union(frame_joins.translate((-frame_x_translate,0,0)))
        )
        
        
        self.corner_joins = joins
        
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_platform()
        self.__make_frame()
        self.__make_corner_joins()
    
    def build(self):
        super().build()
        self.platform = self.platform_bp.build()
        scene = (
            cq.Workplane("XY")
            #.box(self.base_length,self.width-5,self.height)
            .union(self.platform.translate((0,0,(self.height/2)+2.5)))
            .union(self.frame)
            .union(self.corner_joins)
        )
        return scene