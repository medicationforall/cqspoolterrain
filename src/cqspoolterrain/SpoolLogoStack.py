import cadquery as cq
from cadqueryhelper import Base
from cqspoolterrain import Spool

class SpoolLogoStack(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.spool_height = 60.00
        self.spool_radius = 97.50
        self.spool_wall_width = 4.00
        self.spool_cut_radius = 36.50
        self.spool_internal_wall_width = 3.00
        self.stack_levels = 3
        self.logo_text = "test"
        
        self.font_size = 55
        self.font_width = 10
        self.font_center_offset = 0
        self.word_offset = None
        self.render_spool = True
        
        #blueprints
        self.bp_spool = Spool()
        
        #shapes
        self.word_claddings = None
        
    def __make_word_cladding(self, word):
        return cq.Workplane("XY").text(word,self.font_size, self.font_width)
        
    def __make_word_claddings(self):
        if not self.logo_text :
            raise Exception(f'logo_text can not be empty {self.logo_text}')
        words = self.logo_text.split(' ')
        
        self.word_claddings = []
        
        for word in words:
            word_cladding = self.__make_word_cladding(word) 
            self.word_claddings.append(word_cladding)
            
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_spool.height = self.spool_height
        self.bp_spool.radius = self.spool_radius
        self.bp_spool.wall_width = self.spool_wall_width
        self.bp_spool.cut_radius = self.spool_cut_radius
        self.bp_spool.internal_wall_width = self.spool_internal_wall_width
        self.bp_spool.make()
        
        self.__make_word_claddings()
        
        
    def __calculate_stack_levels(self):
        if not self.logo_text :
            raise Exception(f'logo_text can not be empty {self.logo_text}')
        words = self.logo_text.split(' ')
        stack_levels = len(words)
        return stack_levels
        
        
    def __build_spool_stack(self, spool):
        stack_levels = self.__calculate_stack_levels()

        def add_spool(loc):
            r_spool = spool.rotate((1,0,0),(0,0,0),90)
            return r_spool.val().located(loc)
        
        stack = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = 1, 
                ySpacing = self.spool_height,
                xCount = 1, 
                yCount= stack_levels, 
                center = True
            )
            .eachpoint(callback = add_spool)
        )
        
        return stack.rotate((1,0,0),(0,0,0),90)
    
    def __build_spool_words(self):
        stack_levels = self.__calculate_stack_levels()
        word_count = 0
        
        def add_word(loc):
            nonlocal word_count
            word = self.word_claddings.pop().translate((0,0,-1*(self.font_width/2)))
            word_length = word.val().BoundingBox().xlen+10
            
            word_offset = 0
            if self.word_offset:
                word_offset = self.word_offset[word_count]
            
            word_block = (
                cq.Workplane("XY")
                .box(
                    word_length,
                    self.spool_height-(self.spool_wall_width*2),
                    self.font_width/3
                ).translate((word_offset,0,-1*(self.font_width /3)-15))
            )
            word_count += 1
            return word.union(word_block).val().located(loc)
        
        word_stack = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = 1, 
                ySpacing = self.spool_height,
                xCount = 1, 
                yCount= stack_levels, 
                center = True
            )
            .eachpoint(callback = add_word)
        )
        
        return word_stack.rotate((1,0,0),(0,0,0),-90)
        
    def __calculate_font_move(self):
        f_move = (self.bp_spool.radius - self.bp_spool.cut_radius) - self.font_center_offset
        return f_move
        
    def build(self):
        super().build()
        font_move = self.__calculate_font_move()
        spool = self.bp_spool.build()
        spool_no_center = self.bp_spool.build_no_center()

        spool_stack_no_center = self.__build_spool_stack(spool_no_center)        
        spool_stack = self.__build_spool_stack(spool)
        spool_words = self.__build_spool_words()
        
        intersect_cylinder = cq.Workplane("XY").cylinder(self.spool_height*self.__calculate_stack_levels(), self.spool_radius)

        words_intersect = (
            cq.Workplane("XY")
            .union(spool_words.translate((0,-font_move,0)))
            .intersect(intersect_cylinder)
            #.add(spool_no_center)
        )
        
        words_intersect = (
            words_intersect
            .cut(spool_stack_no_center)
            )
        
        scene = (
            cq.Workplane("XY")
            .union(words_intersect)
        )
        
        if self.render_spool:
            scene = scene.union(spool_stack)
        
        return scene