import cadquery as cq
from cqindustry import (
    barrier_straight,
    barrier_curved,
    cut_magnets
)

def make_power_face(
        radius = 10, 
        side_radius = 1.5, 
        base_height = 1.5, 
        side_a_deg_=60, 
        side_b_deg=30, 
        face_rotate=90
    ):
    main = cq.Workplane("XY").circle(radius).extrude(1)
    side = cq.Workplane("XY").circle(side_radius).extrude(1)
    base = cq.Workplane("XY").box(radius,base_height*2,1).translate((0,0,base_height/3))
    outline =  (
        cq.Workplane("XY")
        .union(main)
        .union(side.translate((0,radius,0)))
        .union(side.translate((0,radius,0)).rotate((0,0,1),(0,0,0),-side_a_deg_))
        .union(side.translate((0,radius,0)).rotate((0,0,1),(0,0,0),side_b_deg))
        .union(base.translate((0,-radius,0)))
    ).rotate((0,0,1),(0,0,0),face_rotate)
    return outline.faces("<Z").wires().toPending()

def power_line_straight(length = 75, connector_length=2, connector_radius = 11.5):
    connector_plate = cq.Workplane("XY").cylinder(connector_length, connector_radius).rotate((0,1,0),(0,0,0),90).translate((0,0,connector_radius+.5))
    outline = make_power_face()
    barrier = barrier_straight(
        j_shape = outline,
        length = length
    ).translate((0,0,23/2))

    x_translate = (length/2)-connector_length/2
    barrier_plates = (
        cq.Workplane("XY")
        .union(barrier)
        .union(connector_plate)
        .union(connector_plate.translate((x_translate,0,0)))
        .union(connector_plate.translate((-x_translate,0,0)))
    )

    barrier_plates_magnets = cut_magnets(
        barrier_plates,
        y_offset=0,
        z_lift = 6,
        debug=False
    )

    return barrier_plates_magnets


#---- curved power lines

def __add_connector_with_count(max_count=3):
    connector_count_test = 0

    def add_connector(loc):
        nonlocal connector_count_test
        connector = (
            cq.Workplane("XY")
            .cylinder(2, 11.5)
        )
        
        connector = connector.rotate((1,0,0),(0,0,0),90)
        if connector_count_test == 0:
            connector = connector.translate((0,1,0))
        elif connector_count_test == (max_count-1):
            connector = connector.translate((0,-1,0))
            
        connector_count_test+=1
        return connector.translate((0,0,-0.5)).val().located(loc)
    
    return add_connector

def __add_magnets_with_count(shape, pip_height, max_count=2):
    magnet_count_test = 0

    def add_connector( loc):
        nonlocal magnet_count_test
        nonlocal shape
        nonlocal pip_height
        
        connector = shape.rotate((1,0,0),(0,0,0),90)
        if magnet_count_test == 0:
            connector = connector.translate((0,pip_height/2,0))
        elif magnet_count_test == (max_count-1):
            connector = connector.translate((0,-1*(pip_height/2),0))
            
        magnet_count_test+=1
        return connector.translate((0,0,-0.5)).val().located(loc)
    
    return add_connector

def make_curved_connectors():
    connector_arc =(
        cq.Workplane("XY")
        .polarArray(
            radius  = 75, 
            startAngle  = -90, 
            angle  = 60, 
            count  = 3,
            fill = True,
            rotate = True
        )
        .eachpoint(callback = __add_connector_with_count())
    ).rotate((0,1,0),(0,0,0),90).translate((0,75,0))
    return connector_arc

def make_curved_magnets(pip_height = 2.4, pip_radius = 1.56):
    pip = (
        cq.Workplane("XY")
        .cylinder(pip_height,pip_radius)
        .rotate((0,1,0),(0,0,0),0)
    )

    x_translate = 10/2 +2
    y_translate = -1*(10/2+6.5)+6+pip_radius/2
    z_translate = 0

    magnet_cuts = (
        cq.Workplane("XY")
        .union(pip.translate((
            -x_translate,
            y_translate,
            z_translate
        )))
        .union(pip.translate((
            x_translate,
            y_translate,
            z_translate
        )))
    )

    magnet_arc =(
        cq.Workplane("XY")
        .polarArray(
            radius  = 75, 
            startAngle  = -90, 
            angle  = 60, 
            count  = 2,
            fill = True,
            rotate = True
        )
        .eachpoint(callback = __add_magnets_with_count(magnet_cuts, pip_height))
    ).rotate((0,1,0),(0,0,0),90).translate((0,75,0))
    return magnet_arc


def power_line_curve():
    # --- cylinder connectors
    connector_arc = make_curved_connectors()
    magnet_arc = make_curved_magnets()

    path = (
        cq.Workplane("ZY")
        .ellipseArc(
            75,
            75,
            300,
            rotation_angle=-30
        )
    )
    power_face = make_power_face()

    curve_shape = (
        power_face
        .toPending()
        .sweep(path)
        #.rotate((0,1,0),(0,0,0),90)
        #.translate((x_radius/2,-1*(y_radius/2),0))
    )

    curve_shape_2 = (
        power_face
        .toPending()
        .sweep(path.rotate((1,0,0),(0,0,0),180))
        #.rotate((0,1,0),(0,0,0),90)
        #.translate((x_radius/2,-1*(y_radius/2),0))
    )

    curve_power_line = (
        cq.Workplane("XY")
        .union(curve_shape)
        .union(connector_arc)
        .cut(magnet_arc)
    ).rotate((0,1,0),(0,0,0),90).translate((0,0,10/2+6.5))

    curve_power_line_2 = (
        cq.Workplane("XY")
        .union(curve_shape_2)
        .cut(curve_shape)
        .union(connector_arc.rotate((0,1,0),(0,0,0),180).rotate((0,0,1),(0,0,0),180))
        .cut(magnet_arc.rotate((0,1,0),(0,0,0),180).rotate((0,0,1),(0,0,0),180))
    ).rotate((0,1,0),(0,0,0),90).translate((0,0,10/2+6.5))

    return curve_power_line, curve_power_line_2
