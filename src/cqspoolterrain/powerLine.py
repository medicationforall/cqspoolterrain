import cadquery as cq
from cqindustry import (
    barrier_straight,
    barrier_curved,
    cut_magnets
)

def __make_power_face(
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
    outline = __make_power_face()
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
