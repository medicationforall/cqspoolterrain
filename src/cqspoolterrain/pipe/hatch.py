import cadquery as cq

def hatch(
        connector, 
        radius = 11.5,
        height=2,
        bolt_number = 8, 
        bolt_radius=2, 
        bolt_height=1,
        bolt_padding = -2,
        center_radius = 8,
        center_height=1
    ):
    bolt = (
        cq.Workplane("XY")
        .polygon(6, bolt_radius)
        .extrude(bolt_height)
        .translate((bolt_padding,0,0))
        #.rotate((1,0,0),(0,0,0),-58)
    )
    

    def add_bolt(loc):
        return bolt.val().located(loc)
    
    bolt_arc =(
        cq.Workplane("XY")
        .polarArray(
            radius  = radius, 
            startAngle  = 0, 
            angle  = 360, 
            count  = bolt_number,
            fill = True,
            rotate = True
        )
        .eachpoint(callback = add_bolt)
    )
    
    center_cut = cq.Workplane("XY").cylinder(height, center_radius)
    center = cq.Workplane("XY").cylinder(height, center_radius-1).faces("Z").fillet(height-.01)
    
    return (
        cq.Workplane("XY")
        .union(connector.rotate((0,1,0),(0,0,0),90))
        .add(bolt_arc.translate((0,0,bolt_height)))
        .cut(center_cut.translate((0,0,center_height+.5)))
        .union(center.translate((0,0,center_height)))
    )