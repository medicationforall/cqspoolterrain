import cadquery as cq
import math
from . import Base
from cqterrain import tile

class StairLift(Base):
    def __init__(
            self,
            length = 150,
            width = 75,
            height = 75,
            overlook_tile_size = 10,
            walkway_tile_size = 27,
            tile_height = 2,
            stair_count = 9,
            stair_chamfer = None
        ):
        super().__init__()
        # parameters
        self.length = length
        self.width = width
        self.height = height
        
        self.overlook_tile_size = overlook_tile_size
        self.walkway_tile_size = walkway_tile_size
        self.tile_height = tile_height
        
        self.stair_count = stair_count
        self.stair_chamfer = stair_chamfer
        
        #parts
        self.stairs = None
        self.overlook = None
        self.walkway = None
        
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
            
            if self.stair_chamfer:
                step = step.faces("<Y").edges("Z").chamfer(self.stair_chamfer)
                
            stairs = stairs.union(
                step.translate((
                    stair_length-(stair_interval/2)-stair_interval*i,
                    -1*(self.width/4),
                    -1*(self.height/2)+(stair_interval*(i+1)/2)
                )))
            
        self.stairs = stairs
        
    def _make_tile(self, tile_size):
        result = tile.slot_diagonal(
            tile_size = tile_size,
            height = self.tile_height,
            slot_width = 2,
            slot_height = self.tile_height,
            slot_length_padding = 7,
            slot_width_padding = 2,
            slot_width_padding_modifier = .25
        )
        return result
    
    def _make_floor_tiles(self, length, width, tile_size, padding = 2):
        floor_tile = self._make_tile(tile_size)
        def add_tile(loc):
            return floor_tile.val().located(loc)
        
        padded_tile_size = tile_size+2
        x_count = math.floor((length) / padded_tile_size)
        y_count = math.floor((width) / padded_tile_size)
        
        floor_tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = padded_tile_size, 
                ySpacing = padded_tile_size,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_tile)
        )
        
        outline = cq.Workplane("XY").box(
            x_count*padded_tile_size+padding*1, 
            y_count*padded_tile_size+padding*1, 
            self.tile_height
        )
        return floor_tiles, outline
    
    def __make_overlook(self):
        floor_tiles, outline = self._make_floor_tiles(
            self.length/2, 
            self.width/2, 
            self.overlook_tile_size
        )
        
        overlook = cq.Workplane("XY").box(
            self.length/2,
            self.width/2,
            self.height
        )
        
        self.overlook = (
            overlook
            .cut(outline.translate((0,0,self.height/2 - self.tile_height/2)))
            .union(floor_tiles.translate((0,0,self.height/2 - self.tile_height/2)))
        )
        
    def __make_walkway(self):
        floor_tiles, outline = self._make_floor_tiles(
            self.length, 
            self.width/2,
            self.walkway_tile_size
        )
        walkway = cq.Workplane("XY").box(
            self.length,
            self.width/2,
            self.height
        )
        
        self.walkway = (
            walkway
            .cut(outline.translate((0,0,self.height/2 - self.tile_height/2)))
            .union(floor_tiles.translate((0,0,self.height/2 - self.tile_height/2)))
        )
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_stairs()
        self.__make_overlook()
        self.__make_walkway()
        
    
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.walkway.translate((0,self.width/4,0)))
            .union(self.overlook.translate((-self.length/4,-self.width/4,0)))
            .union(self.stairs)
        )
        #return self.stairs
        return scene